# -*- coding: utf-8 -*-

from py2neo import Graph,Node,walk,Relationship,NodeSelector
import pandas as pd
import sys
import os
os.chdir('E:/课程/知识图谱/第3周/数据库建立与查询')

#英雄列表
hero=pd.read_csv('./hero66666.csv',header=0,encoding='gbk')['name']

#装备列表
weapon=pd.read_excel('./data1.xlsx',header=0)['物品名称']

nodes=list(hero)+list(weapon)

#关系列表
relation=[u'相似',u'克制',u'搭配',u'推荐',u'适合用于对抗','同类互斥']

#英雄属性列表
HP_all=['HP',u'生命值',u'血量',u'血上限']
MP_all=['MP',u'法力值',u'蓝量',u'蓝']
HP_recover_all=[u'HP_recover',u'每5秒回血','回血']
MP_recover_all=[u'MP_recover',u'每5秒回复法力值',u'每5秒回蓝',u'回蓝']
R_cooling_all=['R_cooling',u'大招冷却时间']
R_cost_all=['R_cost',u'大招消耗']
skill_R_all=['R',u'大招']
attack_all=['attack',u'物理攻击',u'攻击力',u'攻击']
attack_range_all=['attack_range',u'攻击距离',u'近战',u'远程']
aa=['defense',u'护甲',u'物理防御']
bb=['skill_passive',u'被动技能',u'被动']
cc=['skill_1',u'一技能',u'1技能',u'技能一',u'技能1']
dd=['skill_2',u'二技能',u'2技能',u'技能二',u'技能2']
ee=['skill_1_cooling',u'1技能冷却时间',u'技能1冷却时间',u'一技能冷却时间',u'技能一冷却时间']
ff=['skill_2_cooling',u'2技能冷却时间',u'技能2冷却时间',u'二技能冷却时间',u'技能二冷却时间']
gg=['skill_1_cost',u'1技能消耗',u'技能1消耗',u'一技能消耗',u'技能一消耗']
hh=['skill_2_cost',u'2技能消耗',u'技能2消耗',u'二技能消耗',u'技能二消耗']
ii=['speed',u'移动速度',u'移速',u'速度']
jj=['tag',u'类型']
hero_property=[aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,HP_all,MP_all,HP_recover_all,MP_recover_all,R_cooling_all,R_cost_all,skill_R_all,attack_all,attack_range_all]
        
#道具属性同义词库
wsx='property	法术吸血	物理吸血	暴击率	法术防御	物理防御	每5秒回蓝	每5秒回血	最大法力	最大生命	减cd	攻击速度	移速	法术攻击	物理攻击'.split('	')

wsx.append(u'被动')
wsx.append(u'主动') 

synonym=hero_property+[wsx] #同义词表

#属性词表
propertys=[s[0] for s in synonym ]





'''
定义查询函数
'''

graph=Graph("http://localhost:7474")
#查询node
def find_node(graph,node_name,output=None):
    s=NodeSelector(graph)  
    try:
        if(output):
            return output(s.select(name=node_name).first())
        else:
            return s.select(name=node_name).first()
    except:
        return '没有这个'+node_name+'节点，查询失败'

find_node(graph,'赵云',dict)

    
#查询node的属性
def find_node_property(graph,node_name,props):
    tmp=find_node(graph,node_name,output=dict)
    if(type(props)==list):
        result={}
        for i in props:
            try:
                result[i]=tmp[i]
            except:
                print('输入的属性'+i+'有误，没有这个属性')
        return result
    else:
        return tmp[props]


find_node_property(graph,'赵云',['skill_1','skill_2'])
find_node_property(graph,'赵云','attack_range')

#查询与节点有特定关系的节点
def find_node_from_rela(graph,node_name,relationship):
    node=find_node(graph,node_name)
    tmp=[]
    try:        
        for n in graph.match(start_node=node,rel_type=relationship):
            tmp.append(n.end_node()["name"])
        return tmp
    except:
        return '输入有误，查询失败'
    
    
find_node_from_rela(graph,'赵云','克制')



#n1=find_node(graph,'赵云')
#n2=find_node(graph,'大乔')
#rel=graph.match_one(start_node=n1,end_node=n2)
#rel.type()
#查询两个节点的关系
def find_rela(graph,node_name_1,node_name_2):
    node_1=find_node(graph,node_name_1)
    node_2=find_node(graph,node_name_2)
    try:
        rel=graph.match_one(start_node=node_1,end_node=node_2)
        return node_name_1+rel.type()+node_name_2
    except:
        try:
            rel=graph.match_one(start_node=node_2,end_node=node_1)
            return node_name_2+rel.type()+node_name_1
        except:
            return node_name_1+'与'+node_name_2+'没有关系'
   
    
find_rela(graph,'赵云','王昭君')  
find_rela(graph,'王昭君','赵云') 
find_rela(graph,'赵云','曹操') 

#查询两个node之间是否存在特定关系
def is_node_rela(graph,node_name_1,node_name_2,rela):
    tmp=find_rela(graph,node_name_1,node_name_2)
    return rela in tmp

is_node_rela(graph,'赵云','大乔','搭配')  

#查询node的某个属性值是否为指定值
def is_node_property(graph,node_name,prop,value):    
    return value==find_node_property(graph,node_name,prop)
 
is_node_property(graph,'赵云','attack_range','近程')
is_node_property(graph,'赵云','attack_range','远程')


'''
查询语句的处理
'''

def get_node(s,nodes):
    node=[h for h in nodes if h in s]
    return node
    
get_node('赵云的基本属性',nodes)
get_node('赵云和曹操谁的攻击力比较强',nodes)

def get_rela(s,relationship):
    rela=[r for r in relationship if r in s]
    return rela

get_rela('赵云克制谁',relation)

def get_property(s,propertys):
    prop=[p for p in propertys if p in s]
    return prop

get_property('赵云和曹操谁的攻击力比较强',propertys)
get_property('赵云和曹操谁的attack比较强',propertys)
           
    
'''
同义词替换
'''
 
def synonym_replace(question,synonym):
    replace_word=[]
    for words in synonym:
        for i in words:
            if(i in question):
                question=question.replace(i,words[0])
                replace_word.append(i)
    return question,replace_word

synonym_replace('赵云的攻击力是多少',synonym)
synonym_replace('铁剑加多少暴击率',synonym)

                
'''
查询模板编写
'''

def search(s,syn,nodes,relation,propertys,graph,output=None):
    node=get_node(s,nodes)
    rela=get_rela(s,relation)
    prop=get_property(s,propertys)
    n=len(node)
    r=len(rela)
    p=len(prop)
    if(all([n==1,r==0,p==0])):
        return find_node(graph,node[0],output=output)
    elif(all([n==1,r==0,p!=0])):
        if(prop[0]=='property'):
            tmp=find_node_property(graph,node[0],prop)['property'].split(' ')
            for t in tmp:
                res=[f for f in syn if f in t]
                if(res):
                    return res
                else:
                    return node[0]+'没有这个属性'                            
        else:
            return find_node_property(graph,node[0],prop)
    elif(all([n==1,r==1,p==0])):
        return find_node_from_rela(graph,node[0],rela[0])
    elif(all([n==2,r==0,p==0])):
        return find_rela(graph,node[0],node[1])
    elif(all([n==2,r==1,p==0])):
        return is_node_rela(graph,node[0],node[1],rela[0])
    else:
        return '查询的问题太复杂，暂时无能为力'                
    
search('赵云和曹操','',nodes,relation,propertys,graph,output=None)        
search('赵云的skill_1','',nodes,relation,propertys,graph,output=None)

question='痛苦面具加多少法术攻击'
s,syn=synonym_replace(question,synonym)
search(s,syn,nodes,relation,propertys,graph,output=None)

#
#if __name__=="__main__": 
#    question=sys.argv[1]
#    s,syn=synonym_replace(question,synonym)
#    return search(s,syn,nodes,relation,propertys,graph,output=None)
    
    
