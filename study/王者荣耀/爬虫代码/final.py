# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:45:32 2018

@author: Administrator
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import re

def get_url(driver,url,node_xpath,action=False,action_node=None):

    #爬取页面
    driver.get(url)
    
    #判断是否需要点击动作
    if(action==True):
        actions = ActionChains(driver)
        click_node=driver.find_element_by_xpath(action_node)
        actions.click(click_node)
        actions.click(click_node)
        actions.perform()
    
    #获取各个英雄/装备的节点
    nodes=driver.find_elements_by_xpath(node_xpath)
    #提取英雄/道具名字和对应的url
    name_list=[]
    url_list=[]
    for node in nodes:
        name_list.append(node.text)
        url_list.append(node.get_attribute('href'))
    #转换为DataFrame格式    
    data=pd.DataFrame({'name':name_list,'url':url_list})

    return data


def get_attr_qq(driver,name,url,index_num,names,urls):

        driver.get(url)
        driver.implicitly_wait(5) 
        data={'name':name,'url':url}           
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
            data[hero_rela[i]]=names[urls==u].values[0]

        return pd.DataFrame(data,index=index_num)

            
def get_attr_17173(driver,name,url,index_num,names,urls):
        driver.get(url)
        driver.implicitly_wait(5) 
        data={'name':name,'url':url} 
        attr_list=['HP','MP','attack','magic_attack','defense','injury_reduction_rate','magic_defense',
                   'magic_injury_reduction_rate','speed','sunder_armor','magic_sunder_armor',
                   'speed_up','crit_rate','crit_effect','vampire','magic_vampire',
                   'cooling_reduce','attack_rank','toughness','HP_recover','MP_recover']
        
        ##获取基本属性
        nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div/span')
        
        if(len(nodes)==len(attr_list)):
            for i in range(len(attr_list)):
                data[attr_list[i]]=nodes[i].text
        else:
            print('爬取'+name+'的属性时出错')
            
        
        #获取出装建议    
        nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/ul/li')
         
        for i in range(len(nodes)):
            data['weapon_'+str(i+1)]=nodes[i].text
            
        #获取tag
        nodes=driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/p/span[3]/span')
        
        for i in range(len(nodes)):
            data['tag_'+str(i+1)]=nodes[i].text 
        return pd.DataFrame(data,index=index_num)

        
def get_attr_4399(driver,name,url,index_num,names,urls):    
        driver.get(url)
        driver.implicitly_wait(5) 
        data={'name':name,'url':url} 
                   
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
        return pd.DataFrame(data,index=index_num)

#url='http://pvp.qq.com/web201605/herodetail/501.shtml'
#x=get_attr_qq(driver,'明世隐',url,[0],hero_data1['name'],hero_data1['url'])   

def get_all_attr(driver,names,urls,source):
    get_attr=eval('get_attr_'+source)
    data=get_attr(driver,names[0],urls[0],[0],names,urls)
    for i in range(1,len(urls)):
        try:
            tmp=get_attr(driver,names[i],urls[i],[i],names,urls)
            data=pd.concat([data,tmp]) 
        except Exception as e:
            print(names[i])
            print(urls[i])
            print(e)
    return data


#test    
#z=get_all_attr(driver,hero_data1['name'][:4],hero_data1['url'][:4],source='qq')
#zz=get_all_attr(driver,hero_data2['name'][:4],hero_data2['url'][:4],source='17173')

if __name__=="__main__": 
    
    driver = webdriver.PhantomJS(executable_path=r'D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')
    
    #获取qq上的英雄列表
    hero_data1=get_url(driver,'http://pvp.qq.com/web201605/herolist.shtml','/html/body/div[3]/div/div/div[2]/div[2]/ul/li/a')
    
    #获取17173上的英雄列表
    hero_data2=get_url(driver,'http://news.17173.com/z/pvp/yxtj/index.shtml','//*[@id="jsheroshow"]/li/a')
    
    #获取4399上的装备列表
    item_data0=get_url(driver,"http://news.4399.com/gonglue/wzlm/daoju/",'//*[@id="hreo_list"]/li/a',action=True,action_node='//*[@id="hero_more"]/a')
    
    data1=get_all_attr(driver,hero_data1['name'],hero_data1['url'],source='qq')
    data2=get_all_attr(driver,hero_data2['name'],hero_data2['url'],source='17173')
    item_data=get_all_attr(driver,item_data0['name'],item_data0['url'],source='4399')
    
    hero_data=data1.merge(data2,on='name',how='outer')
    
    hero_data.to_csv('D:/Python project/王者荣耀/hero.csv')
    item_data.to_csv('D:/Python project/王者荣耀/item.csv')
    
    driver.close()
    
    

