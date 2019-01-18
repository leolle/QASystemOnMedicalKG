# -*- coding: utf-8 -*-
"""
获取英雄列表，以及对应的页面url
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd

driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')

driver.get("http://pvp.qq.com/web201605/herolist.shtml")

heros_node=driver.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div[2]/ul/li/a')

hero_list=[]
url_list=[]
for node in heros_node:
    hero_list.append(node.text)
    url_list.append(node.get_attribute('href'))
    
data=pd.DataFrame({'hero':hero_list,'url1':url_list})

driver.get('http://news.17173.com/z/pvp/yxtj/index.shtml')

nodes=driver.find_elements_by_xpath('//*[@id="jsheroshow"]/li/a')

hero_list=[]
url_list=[]
for node in nodes:
    hero_list.append(node.text)
    url_list.append(node.get_attribute('href'))
    
tmp=pd.DataFrame({'hero':hero_list,'url2':url_list})

data=pd.merge(data,tmp,on='hero')

data.to_csv('D:/Python project/王者荣耀/url.csv')
driver.close() 

##4399
driver.get("http://news.4399.com/gonglue/wzlm/daoju/")
actions = ActionChains(driver)
click_node=driver.find_element_by_xpath('//*[@id="hero_more"]/a')
actions.click(click_node)
actions.click(click_node)
actions.perform()
heros_node=driver.find_elements_by_xpath('//*[@id="hreo_list"]/li/a')

item_list=[]
url_list=[]
for node in heros_node:
    item_list.append(node.text)
    url_list.append(node.get_attribute('href'))
    
data=pd.DataFrame({'item':item_list,'url1':url_list})  
data.to_csv('D:/Python project/王者荣耀/item_url.csv') 