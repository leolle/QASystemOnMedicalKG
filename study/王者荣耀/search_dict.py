# -*- coding: utf-8 -*-
import pandas as pd

'''
节点词库，同义词库
'''

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

 