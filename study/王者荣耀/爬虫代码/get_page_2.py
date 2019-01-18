# -*- coding: utf-8 -*-
"""
17173 英雄详情页面
"""

from selenium import webdriver
import pandas as pd

driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')
url="http://news.17173.com/z/pvp/yxtj/zy/index.shtml"
data={'name':'明世隐','url':url} 

attr_list=['HP','MP','attack','magic_attack','defense','injury_reduction_rate','magic_defense',
           'magic_injury_reduction_rate','speed','sunder_armor','magic_sunder_armor',
           'speed_up','crit_rate','crit_effect','vampire','magic_vampire',
           'cooling_reduce','attack_rank','toughness','HP_recover','MP_recover']


driver.get(url)

##获取基本属性
nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div')


for i in range(len(attr_list)):
    data[attr_list[i]]=nodes[i].text.split('：')[1]
    

#获取出装建议    
nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/ul/li')
 
for i in range(len(nodes)):
    data['weapon_'+str(i+1)]=nodes[i].text
    
#获取tag
nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/p/span[3]/span')

for i in range(len(nodes)):
    data['tag_'+str(i+1)]=nodes[i].text
    

