#!/usr/bin/env python3
# coding: utf-8
import cx_Oracle as cx
import pandas as pd
import requests
from py2neo import Graph, Node
import logging
from ylog import *
from tqdm import *
from py2neo import ClientError

set_level(logging.DEBUG)
console_on()
filelog_on("utils")

from prepare_data.extract_triple import InfoExtr
def ner_api(text):
    url = 'http://192.168.4.30:5011/NERBegin'
    r = requests.post(url, data={'inputStr': text})
    entities = eval(r.text)[0]['entities']
    return entities


def fetch_data():
    conn=cx.connect('enigma/enigma123@192.168.4.30:1521/orcl')

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
    sql_drug_details = """select t2.id, product_name, trad_name, product_name_cn, WOMAN_MEDICINE, TABOO, MEDICINE_INTERACTS, INDICATION, CHILDREN_MEDICINE, AGEDNESS_MEDICINE from kbms.IL_INSTR_FILE_INFO t1
    inner join kbms.KBMS_DRUG_INSTRUCTIONS t2
    on t2.drug_code=t1.id
    """
    df_drug_details = pd.read_sql(sql_drug_details, conn)

    ie = InfoExtr()

    # 脑梗死禁用药
    sql = 'select * from kbms.KBMS_DRUG_TABOO'
    df_taboo = pd.read_sql(sql, conn)
    sql_indication = """select * from kbms.KBMS_DRUG_INDICATIONS where TERM_ID like '%脑梗死%'"""
    df_indications = pd.read_sql(sql_indication, conn)
    df_indications['TERM_ID'] = df_indications['TERM_ID'].astype('str')

    # intravenous_drugs = df_indications[df_indications.TERM_ID=='脑梗死']

    sql_intravenous_drugs = """select product_name, trad_name from 
    kbms.KBMS_DRUG_INSTRUCTIONS where ID in (%s)"""
    intravenous_drugs_code = ','.join(["'%s'" % item for item in df_indications.DRUG_ID.values])
    # sql_intravenous_drugs%intravenous_drugs_code
    df_intravenous_drugs_name = pd.read_sql(sql_intravenous_drugs%intravenous_drugs_code, conn)

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
g = Graph(host="192.168.4.36",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
        http_port=7474,  # neo4j 服务器监听的端口号
        user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
        password="neo4j123")
def create_node(label, nodes):
    count = 0
    for node_name in tqdm(nodes):
        node = Node(label, name=node_name)
        # g.schema.create_uniqueness_constraint(label, node_name)
        try:
            g.create(node)
            count += 1
        except ClientError:
            continue
        # debug(count)
    return


'''创建实体关联边'''
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    count = 0
    # 去重处理
    set_edges = []
    for edge in edges:
        try:
            set_edges.append('###'.join(edge))
        except TypeError:
            continue
    all = len(set(set_edges))
    for edge in tqdm(set(set_edges)):
        edge = edge.split('###')
        p = edge[0]
        q = edge[1]
        if p==q:
            continue
        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            start_node, end_node, p, q, rel_type, rel_name)
        try:
            g.run(query)
            count += 1
            # debug(rel_type)
        except Exception as e:
            info(e)
    return

'''创建知识图谱中心疾病的节点'''
def create_diseases_nodes(disease_infos):
    count = 0
    for disease_dict in tqdm(disease_infos):
        node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                    prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                    easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                    cure_department=disease_dict['cure_department']
                    ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
        g.create(node)
        # count += 1
        # debug(count)
    return