# -*- coding: utf-8 -*-
##code 

import cx_Oracle as cx
import py2neo
from py2neo import Graph,Node,Relationship
import time
g = Graph(
    "http://115.159.65.147:7474", 
    username="neo4j", 
    password="zhucj")
#####----节点导入-----
def f_node_insert(table_name,col_name,label_name):
    g = Graph(
    "http://192.168.5.40:7474", 
    username="neo4j", 
    password="1234")
    t1=time.time()
    conn=cx.connect('kbms','kbms','192.168.5.24:1521/orcl')
    print(conn)
    cur=conn.cursor()
    sql='select {0} AS ENTITY_ID,product_name ENTITY_NAME,trad_name,zc_form,permit_no,production_unit,drug_code from {1}  '.format(col_name,table_name)
    print(sql)
    f=cur.execute(sql)
    tx=g.begin()
    cnt=0
    for node_name in f.fetchall():
        node_name_0=node_name[0]
        node_name_1=node_name[1]
        node_name_2=node_name[2]
        node_name_3=node_name[3]
        node_name_4=node_name[4]
        node_name_5=node_name[5]
        node_name_6=node_name[6]
        node_name_7='DRUG'
        node_name_8='DRUG_FROM_SX'
        node_head={}        
        ###添加属性和节点
        #node_head['labe1l']=node_name_0
        node_head['proper']={}
        node_head['proper']['ENTITY_NAME']=node_name_1
        node_head['proper']['trad_name']=node_name_2
        node_head['proper']['zc_form']=node_name_3
        node_head['proper']['permit_no']=node_name_4
        node_head['proper']['production_unit']=node_name_5
        node_head['proper']['drug_code']=node_name_6
        node_head['proper']['TYPE']=node_name_7
        node_head['proper']['FROM']=node_name_8
        #print(node_head)
        node_insert = Node(label_name,ID=node_name_0,**node_head['proper'])
        ###重复数据不做导入
        #find_code_1 = g.find_one(label=label_name, property_key="name",property_value=node_name_0)
        #relation_insert=Relationship(find_code_1,'TEST',find_code_1)  
        #print(relation_insert)
        #tx.create(relation_insert)
        #print(find_code_1)        
        #if  find_code_1:
        #    continue
        tx.create(node_insert)
        
        #g.merge(node_insert)
        print(node_name_0)
        cnt=cnt+1
    tx.commit()
    time_second=time.time()-t1
    print('节点导入完成,共导入节点{0}个,时间为{1}秒'.format(cnt,time_second))	

f_node_insert('KBMS_DRUG_FROM_SX','ID','DRUG_FROM_SX')
#####---关系导入----

### 输入实体1 所属于列，
### 输入实体2所属列
###驶入关系所属于列
###输入表名
###实体1属于标签
###实体2属于标签

def f_relation_insert(ent1,ent2,rel,tab_name,label1=None,label2=None,sql=None):
    print(label1)
    g = Graph(
    "http://115.159.65.147:7474", 
    username="neo4j", 
    password="zhucj")
    t1=time.time()
    conn=cx.connect('nsyy','uat_NSYY','192.168.0.110:1521/orcl')
    cur=conn.cursor()
    if sql==None:
        f=cur.execute('select {0},{1},{2} from {3} where rownum<=100'.format(ent1,rel,ent2,tab_name))
    else:
        f=cur.execute(sql)
    tx=g.begin()
    t1=time.time()
    cnt=0
    for i in f.fetchall():
        ent1=i[0]
        ent2=i[2]
        rel=i[1]
        print(ent1,ent2,rel)
        left_rel = g.find_one(label=label1, property_key="name",property_value=ent1)
        print(left_rel)
        right_rel = g.find_one(label=label2, property_key="name",property_value=ent2)
        relation_insert=Relationship(left_rel,rel,right_rel)
        tx.create(relation_insert)
        cnt=cnt+1
        tx.commit()
    time_second=time.time()-t1
    print('关系导入完成,共导入关系{0}个,时间为{1}秒'.format(cnt,time_second))
    
#f_relation_insert('table_name','table_name','table_name','user_tables','zhonghua','zhonghua')
    


#http://blog.sina.com.cn/s/blog_d18fc6010102x6sy.html
