# -*- coding: utf-8 -*-
"""
4399 装备详情
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import re

driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')

url='http://news.4399.com/wzlm/daoju/fz/m/760625.html'
driver.get(url)
data={'url':url}

pattern=re.compile('(?<=】).+')

data['item']=pattern.search(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/p[4]').text).group().replace(' ','')
data['item_type']=pattern.search(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/p[5]').text).group().replace(' ','')
data['item_price']=pattern.search(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/p[6]').text).group().replace(' ','')
data['item_attr']=pattern.search(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/p[7]').text).group().replace(' ','')
data['item_passive']=pattern.search(driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[3]/p[8]').text).group().replace(' ','')

attr_list='法术吸血	物理吸血	暴击率	法术防御	物理防御	每5秒回蓝	每5秒回血	最大法力	最大生命	减cd	攻击速度	移速	法术攻击	物理攻击'.split('	')
for a in attr_list:
    if a in data['item_attr']:
        pattern1=re.compile('\d+%?(?='+a+')')
        pattern2=re.compile('(?<='+a+'\+)\d+%?')
        try:
            data[a]=pattern1.search(data['item_attr']).group()
        except:
            data[a]=pattern2.search(data['item_attr']).group()
            
