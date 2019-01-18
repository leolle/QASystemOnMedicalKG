# -*- coding: utf-8 -*-
"""
 官网英雄详情
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import re


driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')

url='http://pvp.qq.com/web201605/herodetail/501.shtml'

driver.get(url)

data={'name':'明世隐','url':url} 


##基本属性
nodes=driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div/div/div[1]/ul/li/span/i')

attr_list=['survival','attack','skill_attack','difficulty']

pattern=re.compile('(\d+/?)+') #使用正则表达式匹配数字
for i in range(len(attr_list)):
    tmp=nodes[i].get_attribute('style')
    data[attr_list[i]]=pattern.search(tmp).group()
    
##技能
nodes=driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/ul/li')

actions=ActionChains(driver)

for i in range(4):
    actions.move_to_element(nodes[i])
    actions.perform()
    data['skill_'+str(i)]=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div['+str(i+1)+']/p[1]/b').text
    tmp=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div['+str(i+1)+']/p[1]/span[1]').text
    data['skill_'+str(i)+'_cooling']=pattern.search(tmp).group()
    tmp=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div['+str(i+1)+']/p[1]/span[2]').text
    data['skill_'+str(i)+'_cost']=pattern.search(tmp).group()
    data['skill_'+str(i)+'_desc']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div['+str(i+1)+']/p[2]').text
    
##英雄关系
nodes=driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div/div[2]/ul/li/a')
hero_rela=['搭配英雄1','搭配英雄2','压制英雄1','压制英雄2','被压制英雄1','被压制英雄2']
for i in range(len(hero_rela)):
    u=nodes[i].get_attribute('href')
    data[hero_rela[i]]=hero_data1['name'][hero_data1['url']==u].values[0]
    #data[hero_rela[i]]=nodes[i].get_attribute('href')

    


    