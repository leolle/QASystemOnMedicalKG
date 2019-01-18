# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:25:55 2018

@author: Administrator
"""

from selenium import webdriver
import pandas as pd

driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')

driver.get("http://news.17173.com/z/pvp/yxtj/zy/index.shtml")

##获取基本属性
nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div')

attr_list=[]
for n in nodes:
    attr_list.append(n.text)

#获取出装建议    
nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/ul/li')
 
item_list=[]
for n in nodes:
    item_list.append(n.text)
    

