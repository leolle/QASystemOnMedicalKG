from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#首先从王者荣耀官网上英雄信息开始
driver = webdriver.PhantomJS()
driver.get('http://pvp.qq.com/web201605/herolist.shtml')
#英雄列表
hero_list = []
#推荐搭配
partner1 = []
partner2 = []
#克制英雄列表
counter1 = []
counter2 = []
#被克制英雄列表
countered1 = []
countered2 = []
hero_number = []
#推荐使用的装备，现在官网有两套推荐出装了
weapon1 = []
weapon2 = []
weapon3 = []
weapon4 = []
weapon5 = []
weapon6 = []
#技能消耗及冷却和说明
skill_1_cd = []
skill_2_cd = []
skill_3_cd = []
skill_1_cost = []
skill_2_cost = []
skill_3_cost = []
skill_1 = []
skill_2 = []
skill_3 = []
skill_0 = []
pic_all = []
hero_num=len(driver.find_elements_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[2]/ul/li/a/img'))
#下面这四个是官网给的英雄参数，之后用来做聚类
shengcun=[]
shanghai=[]
jineng=[]
nandu=[]
for i in range(1, hero_num+1):
    #下面看英文应该知道是什么，都是当前的对象，之后加到各自属于的集合中
    hero_name = driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[2]/ul/li[' + str(i) + ']/a/img').get_attribute('alt')
    hero_list.append(hero_name)
    #因为官网推荐搭配英雄等地方放的都是头像，不直接是名称，但每个英雄都有一个编号，所以先用这个编号来代指英雄
    number = int(driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[2]/ul/li[' + str(i) + ']/a/img').get_attribute('src')[-7:-4])
    hero_number.append(number)
    #加上英雄头像，不过可能也没用
    pic = driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[2]/ul/li[' + str(i) + ']/a/img').get_attribute('src')
    pic_all.append(pic)
    #去英雄的介绍界面
    hero_link = driver.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[2]/ul/li[' + str(i) + ']/a').get_attribute('href')
    driver.get(hero_link)
    #鼠标悬停在各个地方然后爬取信息
    shengcun.append(0.01 * int(re.findall('\d+', driver.find_element_by_xpath(
        '/html/body/div[3]/div[1]/div/div/div[1]/ul/li[1]/span/i').get_attribute('style'))[0]))
    shanghai.append(0.01 * int(re.findall('\d+', driver.find_element_by_xpath(
        '/html/body/div[3]/div[1]/div/div/div[1]/ul/li[2]/span/i').get_attribute('style'))[0]))
    jineng.append(0.01 * int(re.findall('\d+', driver.find_element_by_xpath(
        '/html/body/div[3]/div[1]/div/div/div[1]/ul/li[3]/span/i').get_attribute('style'))[0]))
    nandu.append(0.01 * int(re.findall('\d+', driver.find_element_by_xpath(
        '/html/body/div[3]/div[1]/div/div/div[1]/ul/li[4]/span/i').get_attribute('style'))[0]))
    action = ActionChains(driver)
    action.move_to_element(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/ul/li[1]'))

    partner1.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a/img').get_attribute('src')[
                        -7:-4]))
    partner2.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/ul/li[2]/a/img').get_attribute('src')[
                        -7:-4]))

    action.move_to_element(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/ul/li[2]'))
    counter1.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/ul/li[1]/a/img').get_attribute('src')[
                        -7:-4]))
    counter2.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/ul/li[2]/a/img').get_attribute('src')[
                        -7:-4]))

    action.move_to_element(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/ul/li[3]'))
    countered1.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[3]/div[2]/ul/li[1]/a/img').get_attribute('src')[
                          -7:-4]))
    countered2.append(int(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[3]/div[2]/ul/li[2]/a/img').get_attribute('src')[
                          -7:-4]))

    action.move_to_element(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[1]/ul/li[1]'))
    weapon1.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]/p').text)
    weapon2.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[2]/p').text)
    weapon3.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[3]/p').text)
    weapon4.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[4]/p').text)
    weapon5.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[5]/p').text)
    weapon6.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[1]/ul/li[6]/p').text)
    link = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/ul/li[2]/img')
    ActionChains(driver).move_to_element(link).perform()
    skill_1_cd.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[2]/p[1]/span[1]').text[4:])
    skill_1_cost.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[2]/p[1]/span[2]').text[3:])
    skill_1.append(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[2]/p[1]/b').text + ':' + driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[2]/p[2]').text)

    link = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/ul/li[3]/img')
    ActionChains(driver).move_to_element(link).perform()
    skill_2_cd.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[3]/p[1]/span[1]').text[4:])
    skill_2_cost.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[3]/p[1]/span[2]').text[3:])
    skill_2.append(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[3]/p[1]/b').text + ':' + driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[3]/p[2]').text)
    link = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/ul/li[4]/img')
    ActionChains(driver).move_to_element(link).perform()
    skill_3_cd.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[4]/p[1]/span[1]').text[4:])
    skill_3_cost.append(
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[4]/p[1]/span[2]').text[3:])
    skill_3.append(driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[4]/p[1]/b').text + ':' + driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[4]/p[2]').text)

    link = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/ul/li[1]/img')
    ActionChains(driver).move_to_element(link).perform()
    skill_0.append(driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div/div[1]/p[2]').text)
    driver.get('http://pvp.qq.com/web201605/herolist.shtml')
#把之前的编号变成对应的英雄名称
partner_1=[]
partner_2=[]
counter_1=[]
counter_2=[]
countered_1=[]
countered_2=[]
for i in partner1:
    partner_1.append(hero_list[hero_number.index(i)])
for i in partner2:
    partner_2.append(hero_list[hero_number.index(i)])
for i in counter1:
    counter_1.append(hero_list[hero_number.index(i)])
for i in counter2:
    counter_2.append(hero_list[hero_number.index(i)])
for i in countered1:
    countered_1.append(hero_list[hero_number.index(i)])
for i in countered2:
    countered_2.append(hero_list[hero_number.index(i)])
from time import sleep

#去17173网上爬英雄属性


HP=range(1,hero_num+1)
MP=range(1,hero_num+1)
attack=range(1,hero_num+1)
defense=range(1,hero_num+1)
magic_defense=range(1,hero_num+1)
speed=range(1,hero_num+1)
attack_range=range(1,hero_num+1)
HP_recover=range(1,hero_num+1)
MP_recover=range(1,hero_num+1)
tag_all=range(1,hero_num+1)

driver.get('http://news.17173.com/z/pvp/yxtj')
weapon_num=len(driver.find_elements_by_xpath('//*[@id="jsheroshow"]/li/a/span[1]/img'))
for i in range(1,weapon_num+1):
    hero=driver.find_element_by_xpath('//*[@id="jsheroshow"]/li['+str(i)+']/a/span[1]/img').get_attribute('alt')
    m=hero_list.index(hero)
    link=driver.find_element_by_xpath('//*[@id="jsheroshow"]/li['+str(i)+']/a').get_attribute('href')
    driver.get(link)
    #可能会出现页面没刷出来元素的情况，视情况来调整等待时间
    sleep(3)
    tag_num=len(driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/p/span[3]/span'))
    tag=''
    for j in range(1,tag_num+1):
        tag=tag+' '+driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/p/span[3]/span['+str(j)+']').text+' '
    tag_all[m]=tag
    driver.find_elements_by_xpath('//*[@class="c-tx3"]')[2].text
    HP[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[0].text)
    MP[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[1].text)
    attack[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[2].text)
    defense[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[4].text)
    magic_defense[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[6].text)
    speed[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[8].text)
    attack_range[m]=driver.find_elements_by_xpath('//*[@class="c-tx3"]')[17].text
    HP_recover[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[19].text)
    MP_recover[m]=int(driver.find_elements_by_xpath('//*[@class="c-tx3"]')[20].text)
    driver.get('http://news.17173.com/z/pvp/yxtj')

#把英雄信息做成dataframe进一步转成csv
import pandas as pd
import numpy as np
data=pd.DataFrame({
                'tag':tag_all,
                'HP':HP,
                'MP':MP,
                'attack':attack,
                'defense':defense,
                'magic_defense':magic_defense,
                'speed':speed,
                'HP_recover':HP_recover,
                'MP_recover':MP_recover,
                'attack_range':attack_range,
                'name':hero_list,
                'skill_1':skill_1,
                'skill_1_cooling':skill_1_cd,
                'skill_1_cost':skill_1_cost,
                'skill_2':skill_2,
                'skill_2_cooling':skill_2_cd,
                'skill_2_cost':skill_2_cost,
                'R':skill_3,
                'R_cost':skill_3_cost,
                'R_cooling':skill_3_cd,
                u'搭配英雄1':partner_1,
                u'搭配英雄2': partner_2,
                u'克制英雄1':counter_1,
                u'克制英雄2':counter_2,
                u'被克制英雄1':countered_1,
                u'被克制英雄2':countered_2,
                u'推荐出装1':weapon1,
                u'推荐出装2': weapon2,
                u'推荐出装3': weapon3,
                u'推荐出装4': weapon4,
                u'推荐出装5':weapon5,
                u'推荐出装6':weapon6
                u'生存能力':shengcun,
                u'攻击伤害':shanghai,
                u'上手难度':nandu,
                u'技能效果':jineng
})
#存储英雄的信息
#打开excel可能是乱码，这里有一个小技巧，打开新的excel选择数据-自文本 分隔符号选上，文件原始格式选择65001：unicode（UTF-8)，确定之后分隔符号选逗号
# 之后列数据格式最好选文本，选默认的常规可能出现一些意想不到的错误比如冷却时间是12/8/6可能会被判定为日期
data.to_csv(u'f://英雄信息.csv',index=False,encoding='utf-8')
#爬物品
driver.get('http://pvp.qq.com/web201605/item.shtml#none')
price=[]
shuxing=[]
name=[]
beidong=[]
for i in range(1,94):
    name1=driver.find_element_by_xpath('//*[@id="Jlist-details"]/li['+str(i)+']/a/img').get_attribute('alt')
    name.append(name1)
    link=driver.find_element_by_xpath('//*[@id="Jlist-details"]/li['+str(i)+']/a/img')
    ActionChains(driver).move_to_element(link).perform()
    price1=driver.find_element_by_xpath('//*[@id="Jtprice"]').text[3:]
    price.append(price1)
    #有的物品可能没属性，只有被动如打野刀
    if driver.find_elements_by_xpath('//*[@id="Jitem-desc1"]/p') !=[]:
        shuxing1=driver.find_element_by_xpath('//*[@id="Jitem-desc1"]/p').text
        # 因为属性或者被动可能有好几个，本身是用换行符分开的，如果保留之后excel上看会很不容易看，所以把换行符换成空格，下同
        shuxing.append(shuxing1.replace('\n',' '))
    else :
        shuxing.append('')
    #有的普通装备可能没有被动
    if driver.find_elements_by_xpath('//*[@id="Jitem-desc2"]/p')!=[]:
        a=driver.find_element_by_xpath('//*[@id="Jitem-desc2"]/p').text
        a=a.replace('\n',' ')
        beidong.append(a)
    else:
        beidong.append('')
weapon_data=pd.DataFrame({
    u'物品名称':name,
    u'属性':shuxing,
    u'被动':beidong
})
weapon_data.to_csv(u'f://物品信息.csv',index=False,encoding='utf-8')

#做成三元组  这里先用python把关系写出来 然后用excel整理数据，因为只需要复制粘贴就好，比python容易一点 整理成
hero1=[]
relation=[]
hero2=[]
#英雄间克制搭配关系
for i in range(0,hero_num):
    hero1.append(data[u'name'][i])
    relation.append(u'搭配')
    hero2.append(data[u'搭配英雄1'][i])
    hero1.append(data[u'name'][i])
    relation.append(u'搭配')
    hero2.append(data[u'搭配英雄2'][i])
    hero1.append(data[u'name'][i])
    relation.append(u'克制')
    hero2.append(data[u'克制英雄1'][i])
    hero1.append(data[u'name'][i])
    relation.append(u'克制')
    hero2.append(data[u'克制英雄2'][i])
    hero1.append(data[u'被克制英雄1'][i])
    relation.append(u'克制')
    hero2.append(data[u'name'][i])
    hero1.append(data[u'被克制英雄2'][i])
    relation.append(u'克制')
    hero2.append(data[u'name'][i])
relation1=pd.DataFrame({'实体1':hero1,'实体2':hero2,'关系':relation})
relation1.to_csv(u'f://关系1.csv',encoding='utf-8',index=False)
hero=[]
weapon=[]
relation=[]
for i in range(0,hero_num):
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装1'][i])
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装2'][i])
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装3'][i])
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装4'][i])
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装5'][i])
    hero.append(data[u'name'][i])
    relation.append(u'推荐')
    weapon.append(data[u'推荐出装6'][i])

weapon_data
relation2=pd.DataFrame({'实体1':hero,'实体2':weapon,'关系':relation})
relation2.to_csv(u'f://关系2.csv',encoding='utf-8',index=False)


#判断物品是否适合对抗某英雄具体标准就是很简单的比如有魔抗就适合对抗魔法类英雄
weapon=[]
hero=[]
relation=[]
for i in range(0,hero_num):
    for j in range(0,weapon_num):
        if  (u'法师' in  data['tag'][i] ) & (u'法术防御' in weapon_data[u'属性'][j]+weapon_data[u'被动'][j]):
            hero.append(data['name'][i])
            weapon.append(weapon_data[u'物品名称'][j])
            relation.append(u'适合用于对抗')
        if  ((u'战士' in  data['tag'][i])|(u'射手' in data[u'tag'][i]))&(u'物理防御' in weapon_data[u'属性'][j]+weapon_data[u'被动'][j]):
            hero.append(data['name'][i])
            weapon.append(weapon_data[u'物品名称'][j])
            relation.append(u'适合用于对抗')
        if  (u'坦克' in data['tag'][i])&(u'护甲穿透' in weapon_data[u'属性'][j]+weapon_data[u'被动'][j]):
            hero.append(data['name'][i])
            weapon.append(weapon_data[u'物品名称'][j])
            relation.append(u'适合用于对抗')
        if  (u'坦克' in data['tag'][i])&(u'法术穿透' in weapon_data[u'属性'][j]+weapon_data[u'被动'][j]):
            hero.append(data['name'][i])
            weapon.append(weapon_data[u'物品名称'][j])
            relation.append(u'适合用于对抗')
relation3 = pd.DataFrame({'实体1': hero, '实体2': weapon, '关系': relation})
relation3.to_csv(u'f://关系3.csv',encoding='utf-8',index=False)
#英雄间相似关系我们利用英雄特点和标签进行聚类，然后在同一类即为相似。我们先做一下特征选择，把标签中出现次数太少的比如隐身，然后用标签和英雄数据进行聚类
#先筛选出次数出现太少（少于5次）的
#这个用来存放所有出现的标签，用来统计次数
tag_all_2=[]
tag_number=[]
for i in range(0,hero_num):
    tag1=tag_all[i].split('  ')
    for j in tag1:
        #同义词替换一下
        if j==u'高爆发':
            j=u'爆发'
        if j in tag_all_2:
            tag_number[tag_all_2.index(j)] = tag_number[tag_all_2.index(j)] + 1
        else:
            tag_all_2.append(j)
            tag_number.append(1)
#下面两个数组用来放出现次数超过5次的标签和它们的出现次数
tag_all_3=[]
tag_number_2=[]
for i in range(0,len(tag_all_2)):
    if tag_number[i]>=5:
        tag_all_3.append(tag_all_2[i])
        tag_number_2.append(tag_number[i])
#tag_1 用来存放各英雄是否有某个标签，有即为1，没有即为0，后面再加上英雄的各个参数
tag_1=[]
for i in range(0,hero_num):
    tag_1.append([])
    for j in range(0,len(tag_all_3)):
        if tag_all_3[j] in data['tag'][i]:
            tag_1[i].append(1)
        else:
            tag_1[i].append(0)
    tag_1[i].append(shengcun[i])
    tag_1[i].append(shanghai[i])
    tag_1[i].append(nandu[i])
    tag_1[i].append(jineng[i])
#之后用sklearn的kmeans包聚类找出相似的类,首先用肘方法确定分几类
X=np.array(tag_1)
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
K=range(1,10)
meandistortions=[]
for k in K:
    kmeans=KMeans(n_clusters=k)
    kmeans.fit(X)
    meandistortions.append(sum(np.min(cdist(
            X,kmeans.cluster_centers_,"euclidean"),axis=1))/X.shape[0])
plt.plot(K,meandistortions,'bx-')
plt.xlabel('k')
plt.ylabel(u'平均畸变程度')
plt.title(u'用肘部法则来确定最佳的K值')
#画出图之后选择分成5类 （下降幅度较大虽然和其他比也不太突出，聚类效果可能不是特别好）
relation=[]
hero1=[]
hero2=[]
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=0).fit(tag_1)
for i in range (0,hero_num):
    for j in range(i+1,hero_num):
        if kmeans.labels_[i]==kmeans.labels_[j]:
            relation.append(u'相似')
            hero1.append(data['name'][i])
            hero2.append(data['name'][j])
relation4=pd.DataFrame({u'实体1':hero1,u'关系':relation,u'实体2':hero2})
relation4.to_csv(u'f://关系4.csv',encoding='utf-8',index=False)
#之后用excel把之前得到的关系整理到一起去（复制粘贴就行）然后去重  用Python可能稍微麻烦一点（倒也不难）
