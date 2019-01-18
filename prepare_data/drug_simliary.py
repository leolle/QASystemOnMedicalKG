# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:49:15 2018

@author: zhuchangjiang
"""
#
#import pickle
#path='D:\disease.pkl'
#f=open(path,'rb')
#data1=pickle.load(f)

import cx_Oracle as cx
import pandas as pd
import requests
import json
conn=cx.connect('enigma/enigma123@192.168.4.30:1521/orcl')
def get_input_word(drug_name):
    sql="""select * from (
        select ID, drug_type_name
      FROM (select ID, drug_type_name
              from kbms.kbms_drug_social_insurance t1
            union all
            select ID, CATEGORY_NAME from kbms.KBMS_DRUG_FCT_CATEGORY)
     order by UTL_MATCH.edit_distance_similarity('{0}', drug_type_name) desc)
      where rownum<=100
      """
    data=pd.read_sql(sql.format(drug_name),conn)
    data['input']=drug_name
    sim_values=[]
    for i in range(data.shape[0]):
        word_1=data['DRUG_TYPE_NAME'][i]
        word_2=drug_name
        sim_values.append(sim_text(word_1,word_2))
    data['sim_text']=sim_values
    return data
   
    
def sim_text(word_1,word_2):
    url='http://192.168.4.36:5000/simsent'
    r=requests.post(url,data={'input':word_1+'@@'+word_2})
    result=json.loads(r.text)
    return list(result.values())[0]
    

def get_drug_name(input_word):
    sql_kbms="""
        select T1.ID,T1.CATEGORY_NAME,T3.PRODUCT_NAME
          from kbms.KBMS_DRUG_FCT_CATEGORY t1
          join kbms.KBMS_DRUG_FCT_CATEGORY_SUBITEM t2 on t1.id =
                                                         t2.category_name_id
          join kbms.kbms_drug_instructions t3 on t3.product_name like
                                                 replace(t2.drug_name, '*', '%')
         where T1.ID = '{0}' 
     """
    sql_atc="""
        select distinct t1.id,t1.drug_type_name category_name,t2.drug_name
          from kbms.kbms_drug_social_insurance t1
          join kbms.kbms_drug_social_insurance t2 on t2.code like t1.code || '%'
         where t1.drug_type_name = '{0}'
           and t2.drug_name is not null
    """
    data=get_input_word(input_word)
    result=data.sort_values(['sim_text'],ascending=False).iloc[0]
    if result['ID'].startswith('DN'):
        final=pd.read_sql(sql_kbms.format(result['ID']),conn)
    else:
        final=pd.read_sql(sql_atc.format(result['DRUG_TYPE_NAME']),conn)
    return final


get_drug_name('抗凝血')






















'''

sql_kbms="""
select T1.ID,T1.CATEGORY_NAME,T3.PRODUCT_NAME
  from kbms.KBMS_DRUG_FCT_CATEGORY t1
  join kbms.KBMS_DRUG_FCT_CATEGORY_SUBITEM t2 on t1.id =
                                                 t2.category_name_id
  join kbms.kbms_drug_instructions t3 on t3.product_name like
                                         replace(t2.drug_name, '*', '%')
 where T1.ID = '{0}' 
 """
sql_atc="""
select distinct t1.id,t1.drug_type_name category_name,t2.drug_name
  from kbms.kbms_drug_social_insurance t1
  join kbms.kbms_drug_social_insurance t2 on t2.code like t1.code || '%'
 where t1.drug_type_name = '{0}'
   and t2.drug_name is not null
"""

data=get_input_word('尿激酶')
result=data.sort_values(['sim_text'],ascending=False).iloc[0]
if result['ID'].startswith('DN'):
    final=pd.read_sql(sql_kbms.format(result['ID']),conn)
else:
    final=pd.read_sql(sql_atc.format(result['DRUG_TYPE_NAME']),conn)
'''