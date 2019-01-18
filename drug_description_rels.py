
# coding: utf-8

# ## 1. import modules

# In[1]:

#!/usr/bin/env python3

import cx_Oracle as cx
import pandas as pd
import numpy as np
import os
import json
from py2neo import Graph, Node
import logging
from ylog import *
from tqdm import *
set_level(logging.DEBUG)
console_on()
filelog_on("drugs")


# ## 2. configuration

# In[2]:

conn=cx.connect('enigma/enigma123@192.168.4.30:1521/orcl')


# ## 3. read data from KBMS

# In[3]:

# drugs properly use
sql_drugs = """select t1.product_name, t1.trad_name, t1.id, t1.SMALL_GENERIC_ID,
t2.use_level child_use_level, t2.age_unit child_age_unit, t2.age child_age,
 t3.pregnant_flag, t3.use_level pregnant_use_level,
t4.liver_and_kidney aged_liver_kidney, t4.use_level aged_use_level,
t5.comments  from kbms.KBMS_DRUG_INSTRUCTIONS t1
left join kbms.KBMS_DRUG_CHILD t2 
on t2.DRUG_ID=t1.ID
left join kbms.KBMS_DRUG_PREGNANT t3
on t3.DRUG_ID=t1.ID
left join kbms.KBMS_DRUG_OLDPEOPLE t4
on t4.Drug_Id=t1.id
left join kbms.KBMS_RULE_CHILD_MEDICINE t5
on t1.SMALL_GENERIC_ID=t5.SMALL_GENERIC_ID
"""
sql_drug_details = """select t2.id, t6.term_id, product_name, product_name_cn, WOMAN_MEDICINE, TABOO, MEDICINE_INTERACTS, INDICATION, CHILDREN_MEDICINE, AGEDNESS_MEDICINE from kbms.IL_INSTR_FILE_INFO t1
inner join kbms.KBMS_DRUG_INSTRUCTIONS t2
on t2.drug_code=t1.id
left join kbms.KBMS_DRUG_INDICATIONS t6
on t2.id=t6.drug_id
"""
df_drug_details = pd.read_sql(sql_drug_details, conn)
# df_drugs = pd.read_sql(sql_drugs, conn)


# In[4]:

df_drug_details.shape


# In[5]:

# preview data
df_drug_details.loc[1]


# In[8]:

tmp = df_drug_details.MEDICINE_INTERACTS[1]


# In[9]:

print(tmp)


# ## 4. NER

# In[10]:

import re
import requests
import json
url='http://192.168.4.30:5011/NERBegin'
r=requests.post(url,data={'inputStr':tmp})


# In[11]:

entities=eval(r.text)[0]['entities']


# In[12]:

entities


# In[13]:

df_drug_details.tail()


# ## 5. create entities and relationship

# ### entities

# In[14]:

drug = df_drug_details.loc[1]


# In[15]:

drug


# In[16]:

from prepare_data.extract_triple import InfoExtr, txt_to_json
def ner_api(text):
    url = 'http://192.168.4.30:5011/NERBegin'
    r = requests.post(url, data={'inputStr': text})
    entities = eval(r.text)[0]['entities']
    return entities
ie = InfoExtr()


# In[17]:

str(drug[4])


# In[18]:

input_text = {'选择用药':[drug['PRODUCT_NAME']], '禁忌证':str(drug['MEDICINE_INTERACTS']).split("。")}


# In[19]:

input_text


# In[20]:

output = ie.get_batch(input_text)


# In[21]:

output


# ### create empty lists

# In[22]:

# 共７类节点
ls_diseases = []
ls_drugs = [] # 药品
ls_for_symptom = [] #　适应症
ls_not_for_symptom = []
ls_taboo = [u"老年人", u'儿童', u'孕妇', u'普通人']
# 构建节点实体关系
rels_med_drug_inter = []
rels_med_symp_inter = []
rels_med_symp = []


# In[23]:

drug_dict = {}
data_json = drug
drug_name = data_json['PRODUCT_NAME']
# disease_dict['name'] = disease
ls_drugs.append(drug_name)
drug_dict['symptom'] = ''
#input_text = {'选择用药':[drug['PRODUCT_NAME']], '禁忌证':str(drug['MEDICINE_INTERACTS']).split("。")}
#output = ie.get_batch(input_text)


# In[24]:

df_drug_details_groupby = df_drug_details.groupby('PRODUCT_NAME')
len(df_drug_details_groupby)

df_drug_details_groupby.groups
# In[25]:

df_drug = df_drug_details.loc[df_drug_details_groupby.groups['止嗽化痰颗粒']]
df_drug


# In[26]:

df_drug[['PRODUCT_NAME', 'TERM_ID']].values.tolist()


# In[27]:

df_drug['TERM_ID'].values.tolist()


# In[ ]:

# parse data
for group in tqdm(df_drug_details_groupby.groups):
    debug(group)
    df_drug = df_drug_details.loc[df_drug_details_groupby.groups[group]]
    ls_for_symptom += df_drug['TERM_ID'].values.tolist()
    rels_med_symp += df_drug[['PRODUCT_NAME', 'TERM_ID']].values.tolist()
    drug_name = group
    ls_drugs.append(drug_name)
    # debug('symptom: %s' % df_drug['TERM_ID'].values.tolist())
    # debug('drug: %s' % drug_name)
    try:
        drug = df_drug.iloc[0,:]
        input_text = {'选择用药':[drug['PRODUCT_NAME']], '禁忌证':str(drug['MEDICINE_INTERACTS']).split("。")}
        output = ie.get_batch(input_text)

        if 'drug' in output['禁忌']:
            ls_drugs += output['禁忌']['drug']
            for d in output['禁忌']['drug']:
                rels_med_drug_inter.append([drug_name, d])
        if 'symptom' in output['禁忌']:
            ls_not_for_symptom += output['禁忌']['symptom']
            for d in output['禁忌']['symptom']:
                rels_med_symp_inter.append([drug_name, d])
    except UnicodeDecodeError as e:
        info(e)
        continue

# In[155]:

ls_for_symptom


# In[156]:

ls_not_for_symptom


# In[103]:

ls_drugs


# In[157]:

rels_med_symp_inter


# In[158]:

rels_med_drug_inter


# In[159]:

rels_med_symp

# ### 用药注意事项

# In[28]:

# 儿童禁忌， use level
# "0 - 无
# 1 - 慎用
# 2 - 禁用"
# age unit
# "Y - 年
# M - 月
# D - 日
# H - 时"
sql_taboo_child = """select t2.product_name, t2.trad_name, t1.age, t1.age_unit, t1.use_level from kbms.KBMS_DRUG_CHILD t1
inner join kbms.KBMS_DRUG_INSTRUCTIONS t2 
on t1.DRUG_ID=t2.ID
"""
df_taboo_child = pd.read_sql(sql_taboo_child, conn)

# 孕妇禁忌， use level
# "0 - 无
# 1 - 慎用
# 2 - 禁用"
sql_taboo_pregnant = """select t2.product_name, t2.trad_name, t1.pregnant_flag, t1.use_level from kbms.KBMS_DRUG_PREGNANT t1
inner join kbms.KBMS_DRUG_INSTRUCTIONS t2 
on t1.DRUG_ID=t2.ID"""
df_taboo_pregnant = pd.read_sql(sql_taboo_pregnant, conn)

# 老人禁忌， use level
# "0 - 无
# 1 - 慎用
# 2 - 禁用"
sql_taboo_the_aged = """select t2.product_name, t2.trad_name, t1.liver_and_kidney, t1.use_level from kbms.KBMS_DRUG_OLDPEOPLE t1
inner join kbms.KBMS_DRUG_INSTRUCTIONS t2 
on t1.DRUG_ID=t2.ID"""
df_taboo_the_aged = pd.read_sql(sql_taboo_the_aged, conn)

# 儿童专用
sql_child_only = """select t2.product_name, t2.trad_name, t2.id, t2.SMALL_GENERIC_ID from kbms.KBMS_RULE_CHILD_MEDICINE t1
inner join kbms.KBMS_DRUG_INSTRUCTIONS t2 
on t1.SMALL_GENERIC_ID=t2.SMALL_GENERIC_ID
"""
df_child_only = pd.read_sql(sql_child_only, conn)


# In[32]:



# In[45]:

rels_taboo_child = []
rels_taboo_pregnant = []
rels_taboo_aged = []
rels_child_only = []
# [u"老年人", u'儿童', u'孕妇', u'普通人']
for idx, data in df_taboo_child.iterrows():
    if data['USE_LEVEL'] is not '0':
        rels_taboo_child.append([data['PRODUCT_NAME'], '儿童'])


# In[46]:




# In[44]:

len(rels_taboo_child)


# In[47]:

for idx, data in df_taboo_pregnant.iterrows():
    if data['USE_LEVEL'] is not '0':
        rels_taboo_pregnant.append([data['PRODUCT_NAME'], '孕妇'])


# In[48]:




# In[43]:

len(rels_taboo_pregnant)


# In[62]:

for idx, data in df_taboo_the_aged.iterrows():
    if data['USE_LEVEL'] is not '0':
        rels_taboo_aged.append([data['PRODUCT_NAME'], '老年人'])


# In[50]:




# In[42]:

len(rels_taboo_aged)


# In[58]:

for idx, data in df_child_only.iterrows():
    rels_child_only.append([data['PRODUCT_NAME'], '儿童'])


# In[59]:




# In[60]:

len(rels_child_only)

df_drug_effect_category = pd.read_excel('./data/ATC.xlsx',[0,1])
rels_med_cat = [] # medicine categories/effect relationship
ls_med_cat_effect = []
for idx in range(len(df_drug_effect_category[0])):
    drug = df_drug_effect_category[0].iloc[idx,:]
    drug_name = drug['西药药品名称']
    ls_med_cat_effect += drug[['ATC1名称', 'ATC2名称', 'ATC3名称', '药品分类名称']].values.tolist()
    ls_drugs.append(drug_name)
    rels_med_cat.append([drug_name, drug['ATC1名称']])
    rels_med_cat.append([drug_name, drug['ATC2名称']])
    rels_med_cat.append([drug_name, drug['ATC3名称']])
    rels_med_cat.append([drug_name, drug['药品分类名称']])
for idx in range(len(df_drug_effect_category[1])):
    drug = df_drug_effect_category[1].iloc[idx,:]
    drug_name = drug['中成药药品名称']
    ls_med_cat_effect += drug[['分类1名称', '分类2名称', '分类3名称', '中成药药品类别']].values.tolist()
    ls_drugs.append(drug_name)
    rels_med_cat.append([drug_name, drug['分类1名称']])
    rels_med_cat.append([drug_name, drug['分类2名称']])
    rels_med_cat.append([drug_name, drug['分类3名称']])
    rels_med_cat.append([drug_name, drug['中成药药品类别']])


# In[70]:

dict_drugs = {'ls_diseases':ls_diseases,'ls_drugs':ls_drugs, 'ls_for_symptom':ls_for_symptom,
'ls_not_for_symptom':ls_not_for_symptom, 'ls_taboo':ls_taboo,'rels_med_drug_inter':rels_med_drug_inter,
'rels_med_symp_inter':rels_med_symp_inter,'rels_med_symp':rels_med_symp, 'rels_taboo_child':rels_taboo_child,
             'rels_taboo_pregnant':rels_taboo_pregnant, 'rels_taboo_aged':rels_taboo_aged,'rels_child_only':rels_child_only,
              'rels_med_cat':rels_med_cat, 'ls_med_cat_effect':ls_med_cat_effect}


# In[71]:

dict_drugs


# In[75]:

debug('rels done!')


# In[76]:

debug('dumping dict...')


# In[72]:

import pickle
with open('./data/drug_nodes_rels.pkl', 'wb') as f:
    pickle.dump(dict_drugs, f)


# In[73]:

with open('./data/drug_nodes_rels.pkl', 'rb') as f:
    k = pickle.load(f)


# In[ ]:



