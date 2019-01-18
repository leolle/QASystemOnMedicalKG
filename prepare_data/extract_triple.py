#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import json
import pickle


key_dict = {
            '医保疾病' : 'yibao_status',
            "患病比例" : "get_prob",
            "易感人群" : "easy_get",
            "传染方式" : "get_way",
            "就诊科室" : "cure_department",
            "治疗方式" : "cure_way",
            "治疗周期" : "cure_lasttime",
            "治愈率" : "cured_prob",
            '药品明细': 'drug_detail',
            '药品推荐': 'recommand_drug',
            '推荐': 'recommand_eat',
            '忌食': 'not_eat',
            '宜食': 'do_eat',
            '症状': 'symptom',
            '检查': 'check',
            '成因': 'cause',
            '预防措施': 'prevent',
            '所属类别': 'category',
            '简介': 'desc',
            '名称': 'name',
            '常用药品' : 'common_drug',
            '治疗费用': 'cost_money',
            '并发症': 'acompany'
        }

I63 = {
  "_id": {
    "$oid": "5bb578ce831b973a137e48ac"
  },
  "name": "脑梗死",
  "desc": "脑梗死(cerebralinfarction，CI)是缺血性卒中(ischemicstroke)的总称，包括脑血栓形成、腔隙性梗死和脑栓塞等，约占全部脑卒中的70%，是脑血液供应障碍引起脑部病变。脑梗死是由于脑组织局部供血动脉血流的突然减少或停止，造成该血管供血区的脑组织缺血、缺氧导致脑组织坏死、软化，并伴有相应部位的临床症状和体征，如偏瘫、失语等神经功能缺失的症候，脑梗死发病24～48h后，脑CT扫描可见相应部位的低密度灶，边界欠清晰，可有一定的占位效应。脑MRI检查能较早期发现脑梗死，表现为加权图像上T1在病灶区呈低信号，T2呈高信号，MRI能发现较小的梗死病灶。\n临床上许多人即使具备上述脑血管病危险因素却没有发生脑血管病，而另外一些不具备上述脑血管病危险因素的人却患了脑血管病，说明脑血管病的发生还与其他因素有关，尤其是遗传因素有关。脑血管病家族史可能是脑血管病的危险因素，有实验也证明有高血压，糖尿病病史者的发病率和有脑血管病家族史的，发病人数均显著高于对照组，一般认为多数的脑血管病的发病是多因素的，是遗传与环境因素共同作用的结果，如脑血管病的发病率有一定的种族差异，黑种人脑血管病发病率高于白种人。",
  "category": [
    "疾病百科",
    "内科",
    "神经内科"
  ],
  "prevent": "针对可能的病因，积极预防，加强对动脉粥样硬化，高脂血症，高血压，糖尿病等疾病的防治。\n1.对于高血压患者，应将血压控制在一个合理水平，因为血压过高，易使脑内微血管瘤及粥样硬化的小动脉破裂出血;而血压过低，脑供血不全，微循环淤滞时，易形成脑梗死，所以应防止引起血压急骤降低，脑血流缓慢，血黏度增加，以及血凝固性增高的各种因素。\n2.积极治疗短暂性脑缺血发作。\n3.讲究精神心理卫生，许多脑梗死的发作，都与情绪激动有关。\n4.注意改变不良生活习惯，适度的体育活动有益健康，避免不良嗜好如吸烟，酗酒，暴饮，暴食，要以低脂肪低热量，低盐饮食为主，并要有足够优质的蛋白质，维生素，纤维素及微量元素，饮食过饱不利于健康，霉变的食品，咸鱼，冷食品，均不符合食品卫生的要求，要禁食。\n5.当气温骤变，气压，温度明显变化时，由于中老年人特别是体弱多病者，多半不适应而患病，尤其是严寒和盛夏时老年人适应能力差，免疫能力降低，发病率及死亡率均比平时高，所以要特别小心。\n6.及时注意脑血管病的先兆，如突发的一侧面部或上，下肢突然感到麻木，软弱乏力，嘴歪，流口水;突然感到眩晕，摇晃不定;短暂的意识不清或嗜睡等。",
  "cause": "一、发病原因\n1、血管壁本身的病变(25%)：\n最常见的是动脉粥样硬化，且常常伴有高血压、糖尿病、高脂血症等危险因素。其可导致各处脑动脉狭窄或闭塞性病变，但以大中型管径(≥500μm)的动脉受累为主，国人的颅内动脉病变较颅外动脉病变更多见。其次为脑动脉壁炎症，如结核、梅毒、结缔组织病等。此外，先天性血管畸形、血管壁发育不良等也可引起脑梗死。由于动脉粥样硬化好发于大血管的分叉处和弯曲处，故脑血栓形成的好发部位为颈动脉的起始部和虹吸部、大脑中动脉起始部、椎动脉及基底动脉中下段等。当这些部位的血管内膜上的斑块破裂后，血小板和纤维素等血液中有形成分随后黏附、聚集、沉积形成血栓，而血栓脱落形成栓子可阻塞远端动脉导致脑梗死。脑动脉斑块也可造成管腔本身的明显狭窄或闭塞，引起灌注区域内的血液压力下降、血流速度减慢和血液黏度增加，进而产生局部脑区域供血减少或促进局部血栓形成出现脑梗死症状。 [1]\n2、血液成分改变(22%)：\n真性红细胞增多症、高黏血症、高纤维蛋白原血症、血小板增多症、口服避孕药等均可致血栓形成。少数病例可有高水平的抗磷脂抗体、蛋白C、蛋白S或抗血栓Ⅲ缺乏伴发的高凝状态等。这些因素也可以造成脑动脉内的栓塞事件发生或原位脑动脉血栓形成。\n3、不良生活习惯(25%)：\n①吸烟，酗酒：在脑血管病患者中吸烟人数显著高于非脑血管病患者的对照组，并且每天吸烟与脑血管病的发生呈正相关，酗酒肯定是不良生活习性，酗酒是高血压显著的危险因素，而高血压是最重要的脑血管病的危险因素。\n②便秘：中医认为，脑血管病的发病具有一定的规律性，与便秘可能相关，应通过饮食结构调整及养成规律性排便习惯，有助于降低脑血管病发生的可能性。\n③体育锻炼，超重与脑血管病：在脑血管病患者中平时进行体育锻炼的人数比例显著低于非脑血管病对照组，而脑血管病超重人数显著高于非脑血管病对照组，因此平衡饮食，控制体重与体育锻炼相结合，可以降低发生脑血管病的发病率。\n④高盐饮食：一般认为高盐饮食是高血压的危险因素，高血压是最重要的脑血管病的危险因素，故提倡低盐饮食，饮食中可适当增加醋的摄入量以利于钙的吸收。\n4、遗传家族史(10%)：\n临床上许多人即使具备上述脑血管病危险因素却没有发生脑血管病，而另外一些不具备上述脑血管病危险因素的人却患了脑血管病，说明脑血管病的发生还与其他因素有关，尤其是遗传因素有关。脑血管病家族史可能是脑血管病的危险因素，有实验也证明有高血压，糖尿病病史者的发病率和有脑血管病家族史的，发病人数均显著高于对照组，一般认为多数的脑血管病的发病是多因素的，是遗传与环境因素共同作用的结果，如脑血管病的发病率有一定的种族差异，黑种人脑血管病发病率高于白种人。\n二、病理改变\n(1)急性脑梗死灶的中央区为坏死脑组织，周围为水肿区，在梗死的早期脑水肿明显，梗死面积大者，水肿也明显，相反梗死面积小者，水肿面积相对较小，水肿区脑回变平，脑沟消失，当梗死面积大，整个脑半球水肿时，中线结构移位，严重病例可有脑疝形成，后期病变组织萎缩，坏死组织由格子细胞清除，留下有空腔的瘢痕组织，陈旧的血栓内可见机化和管腔再通，动脉硬化性脑梗死一般为白色梗死，少数梗死区的坏死血管可继发性破裂而引起出血，称出血性梗死或红色梗死。\n(2)病生理变化：\n①血管活性物质的含量变化：脑梗死者肿瘤坏死因子含量明显增高，此外NO，内皮素，降钙素基因相关肽，神经肽Y也均随之增高，神经肽Y和神经降压素是对心脑血管系统具有重要调控作用的神经内分泌多肽，急性脑血管病发病过程中，肿瘤坏死因子，一氧化氮，内皮素，神经肽Y，降钙素基因相关肽和神经降压素发生变化，这种变化与急性脑血管病的疾病性质，病情有密切关系，积极控制这些物质之间的平衡紊乱，将有助于降低急性脑血管病的病死率和致残率。\n②下丘脑-垂体激素的释放：神经与内分泌两大系统各有其特点又密切相关，共同调控和整合内，外环境的平衡，脑血管病患者下丘脑-垂体激素的释放增强，这种释放可能直接侵犯至下丘脑，垂体等组织，或与脑水肿压迫血管使有关组织循环障碍有关。\n③血浆凝血因子的变化：凝血因子Ⅶ(FⅦ)活性增高为缺血性脑血管病的危险因子，甚或与心肌梗死及猝死相关。\n④一氧化氮的变化：一氧化氮(NO)的作用与其产生的时间，组织来源及含量等有关，内皮细胞上有组织型一氧化氮合成酶(cNOS)，在脑梗死早期它依赖于钙/钙调素(Ca2 /CaM)激活，引起NO短期释放，使血管扩张，产生有益作用，另外，在巨噬细胞，胶质细胞上的诱生型NOS(iNOS)，它不依赖于Ca2 /CaM，在生理状态下不激活，脑梗死后1～2天，iNOS被激活，一旦被激活，则不断产生NO，持续性NO产生可引起细胞毒性作用，所以在脑梗死急性期，iNOS被激活，可能加重缺血性损害。\n⑤下丘脑-垂体-性腺轴的改变：急性脑血管病可导致下丘脑-垂体-性腺轴的功能改变，不同的性别，不同的疾病类型其性激素的变化是不相同的。\n急性脑血管病导致机体内分泌功能紊乱的因素主要表现为：①与神经递质的调节障碍有关的性腺激素类：多巴胺，去甲肾上腺素和5-羟色胺分泌增加，单胺代谢出现紊乱，导致性激素水平变化，使雌激素水平降低，②应激反应：机体处于应激状态能通过自身对内分泌进行调节。\n另外，临床上许多人即使具备脑血管病的危险因素，却未发生脑血管病，而一些不具备脑血管病危险因素的人却发生脑血管病，说明脑血管病的发生可能还与其他因素有关，如遗传因素和不良嗜好等。\n流行病学研究证实，高血脂和高血压是动脉粥样硬化的两个主要危险因素，吸烟，饮酒，糖尿病，肥胖，高密度脂蛋白胆固醇降低，三酰甘油增高，血清脂蛋白增高均为脑血管病的危险因素，尤其是缺血性脑血管病的危险因素。",
  "symptom": [
    "昏迷",
    "精神障碍",
    "脑缺血",
    "颅内压增高",
    "恶心",
    "眼肌麻痹",
    "复视",
    "感觉障碍"
  ],
  "yibao_status": "否",
  "get_prob": "0.1%",
  "easy_get": "50～60岁以上的人群",
  "get_way": "无传染性",
  "acompany": [
    "脑性瘫痪"
  ],
  "cure_department": [
    "内科",
    "神经内科"
  ],
  "cure_way": [
    "手术治疗",
    "介入治疗",
    "药物治疗",
    "支持性治疗"
  ],
  "cure_lasttime": "1-2年",
  "cured_prob": "60%",
  "common_drug": [
    "通脉颗粒",
    "灯银脑通胶囊"
  ],
  "cost_money": "根据不同医院，收费标准不一致，市三甲医院约（3000——10000元）",
  "check": [
    "血常规",
    "尿常规",
    "便常规",
    "血液生化六项检查",
    "颅脑MRI检查",
    "血浆激肽释放酶原测定",
    "脑脊液乳酸",
    "脑血流显像",
    "脑脊液肌酸激酶",
    "纤维蛋白原"
  ],
  "do_eat": [
    "鸭翅",
    "莲子",
    "核桃",
    "青豆"
  ],
  "not_eat": [
    "鸭肝",
    "芝麻",
    "杏仁",
    "松子仁"
  ],
  "recommand_eat": [
    "羊肉汤面",
    "羊肉温补汤",
    "温养脾胃带鱼汤",
    "红烧带鱼",
    "黄豆芽蘑菇汤",
    "炝黄豆芽",
    "素炒黄豆芽",
    "黄豆芽炖豆腐"
  ],
  "recommand_drug": [
    "大活络丸",
    "银杏叶片",
    "血塞通软胶囊",
    "甲磺酸二氢麦角碱缓释胶囊",
    "长春西汀片",
    "灯银脑通胶囊",
    "银杏达莫注射液",
    "脑心通胶囊",
    "蚓激酶肠溶胶囊",
    "血塞通片",
    "双嘧达莫片",
    "脑塞通丸",
    "脑脉泰胶囊",
    "藻酸双酯钠片",
    "曲克芦丁片",
    "复方丹蛭片",
    "通脉颗粒"
  ],
  "drug_detail": [
    "百灵鸟通脉颗粒(通脉颗粒)",
    "络泰灯银脑通胶囊(灯银脑通胶囊)",
    "多力康(长春西汀片)",
    "上海杏灵科技银杏叶片(银杏叶片)",
    "络泰血塞通软胶囊(血塞通软胶囊)",
    "中联大活络丸(大活络丸)",
    "东方龙大活络丸(大活络丸)",
    "山西普德银杏达莫注射液(银杏达莫注射液)",
    "御大夫通脉颗粒(通脉颗粒)",
    "步长脑心通胶囊(脑心通胶囊)",
    "普恩复(蚓激酶肠溶胶囊)",
    "培磊能(甲磺酸二氢麦角碱缓释胶囊)",
    "昆明制药血塞通片(血塞通片)",
    "辽宁金丹通脉颗粒(通脉颗粒)",
    "甘肃金羚通脉颗粒(通脉颗粒)",
    "摩美得脑塞通丸(脑塞通丸)",
    "春花牌复方丹蛭片(复方丹蛭片)",
    "山东仁和堂双嘧达莫片(双嘧达莫片)",
    "桂林三金脑脉泰胶囊(脑脉泰胶囊)",
    "石家庄康力藻酸双酯钠片(藻酸双酯钠片)",
    "江苏联环蚓激酶肠溶胶囊(蚓激酶肠溶胶囊)",
    "江苏联环曲克芦丁片(曲克芦丁片)",
    "健民叶开泰国药银杏叶片(银杏叶片)"
  ]
}


def txt_to_json(txt):
    str_appliable_target = '（一）适用对象。'
    str_diagnostic_basis = '（二）诊断依据。'
    str_cure_plan = '（三）治疗方案选择依据。'
    str_recommend_hospitalization_days = '（四）标准住院日为'
    str_checkin_condition = '（五）进入路径标准。'
    str_check_items = '（六）住院后检查项目。'
    str_recommend_drug = '（七）选择用药。'
    str_checkout_condition = '（八）出院标准。'
    str_failure_condition = '（九）退出路径。'
    str_pathway_table = '二、脑梗死临床路径表单'
    str_contradiction = '（九）禁忌证。'
    strings_pattern = '|'.join([str_appliable_target,
                                str_diagnostic_basis,
                                str_cure_plan,
                                str_recommend_hospitalization_days,
                                str_checkin_condition,
                                str_check_items,
                                str_recommend_drug,
                                str_checkout_condition,
                                str_failure_condition,
                                str_contradiction,
                                str_pathway_table
                                ])
    key_word = re.findall(strings_pattern, txt)
    patten = '|'.join(key_word)
    txt_list = re.split(patten, txt)
    txt_dict = {}
    for i in range(len(key_word)):
        # parse key
        key = key_word[i]
        re_key = re.compile("""(）|、)([\u4e00-\u9fa5]+)""") # strip numbering like （一）适用对象。
        key = re_key.search(key).groups()[1]
        # parse value
        value = txt_list[i + 1].split('\n') # split new lines
        value = [x.replace("。", '') for x in value if x]
        # ls_value = []
        # if len(value) > 1:
        #     re_item = re.compile("""^[0-9]+.\s?([\u4e00-\u9fa5\S\w]+)""")
        #     for x in value:
        #         if x:
        #             try:
        #                 ls_value.append(re_item.search(x).group(1))
        #             except AttributeError:
        #                 pass
        # else:
        #     ls_value = value[0].replace("。", '')
        txt_dict[key] = value
    return txt_dict


class InfoExtr():
  def __init__(self):
    self.url = 'http://192.168.4.30:5011/NERBegin'

  def ner_api(self, text):
    '''调用实体识别'''
    r = requests.post(self.url, data={'inputStr': text})
    entities = eval(r.text)[0]['entities']
    return entities

  def parse_hospital_diagnose(self, text):
    """
    入院诊断
    :param text:
    :return:
    """
    if text != '':
      diagnose_entities = re.split('\d\)?（?', text)
      diagnose_entities = [re.sub('[ \t\n]', '', i) for i in diagnose_entities if len(i.replace(' ', '')) >= 2]
    return diagnose_entities

  def parse_medical_orders(self, text):
    '''解析医嘱，直接调用实体识别'''
    medical_text = text
    entities = self.ner_api(medical_text)
    entities = [{i['word']: i['type']} for i in entities if i['type'] in ['DRU', 'TES'] and i['word'] != '服药']
    return entities

  def parse_physical_examination(self, text):
    '''查体的结果'''
    ##体温
    try:
      temperature = re.search('(T：?\d{2}\.*?\d)℃', text)
      temperature = temperature.group(1)
    except:
      temperature = ''
    ##心律
    try:
      pulse = re.search('(P：?\d{2}[次/分]?)', text)
      pulse = pulse.group(1)
    except:
      pulse = ''
    ##呼吸
    try:
      respiratory = re.search('(R：?\d{2}[次/分]?)', text)
      respiratory = respiratory.group(1)
    except:
      respiratory = ''
    try:
      blood_pressure = re.search('(BP：?\d{2,3}\/?\d{2,3}mmHg)', text)
      blood_pressure = blood_pressure.group(1)
    except:
      blood_pressure = ''
    return [{'体温': temperature, '脉搏': pulse, '呼吸': respiratory, '血压': blood_pressure}]

  def parse_complain(self, text):
    """
    主诉
    :param text:
    :return:
    """
    try:
      complain = re.search('以([\s\S]{3,30}?)入院', text)
      complain = complain.group(1)
      complain_ner = self.ner_api(complain)
      complain_ner = [{i['word']: i['type']} for i in complain_ner if i['type'] in ('SYM', 'DIS')]
      if len(complain_ner) > 0:
        return complain_ner
      else:
        return complain
    except:
      complain = ''
    return complain

  def parse_ryqk(self, text):
    """
    入院情况
    :param text:
    :return:
    """
    text = re.sub('以([\s\S]{3,30}?)入院', '', text)
    text = re.sub('既往[\s\S]{3,30}?[史。]', '', text)
    all_ner = [{i['word']: i['type']} for i in self.ner_api(text) if
               i['type'] in ['DRU', 'SGN', 'TES'] and len(i['word']) >= 2]
    for i in all_ner:
      if i in ['BP', '查体 :T']:
        del all_ner[i]
    return all_ner

  def parse_hzxx(self, text):
    """
    患者姓名
    :param text:
    :return:
    """
    text = text.split('\t')
    hzxx_dict = {}
    if len(text) == 1:
      return text
    for ner in text:
      a = ner.split('：')
      if len(a) == 1:
        hzxx_dict['患者姓名'] = a[0]
      else:
        hzxx_dict[a[0]] = a[1]
    return hzxx_dict

  def parse_his_dis(self, text):
    """
    既往史
    :param text:
    :return:
    """
    try:
      his_dis = re.search('既往[\s\S]{3,30}?[史。]', text)
      his_dis = his_dis.group(0)
      entities = self.ner_api(his_dis)
      entities = [{i['word']: i['type']} for i in entities if
                  i['type'] in ['DRU', 'TES', 'DIS', 'SYM', 'PT'] and i['word'] != '既往有']
      if len(entities) > 0:
        return entities
      else:
        return [{i: 'DIS'} for i in re.split('[， ]', his_dis)]
    except:
      his_dis = ''
    return his_dis

  def parse_appliable_target(self, text):
      """
      适用对象
      :param text:
      :return:
      """
      try:
          for element in text:
              appliable_target = re.search('ICD-10：([0-9A-Z.]+)', element).group(1)
              if appliable_target:
                  return appliable_target
      except:
          appliable_target = ''
      return appliable_target

  def parse_diagnostic_basis(self, text):
    """
    诊断依据
    :param text:
    :return:
    """
    diagnostic_basis = text.split('\n')  # split new lines
    diagnostic_basis = [x.replace("。", '').replace(" ", '') for x in diagnostic_basis if x]
    ls_value = []
    if len(diagnostic_basis) > 0:
        # re_item = re.compile("""^[0-9]+.\s?([\u4e00-\u9fa5\S\w]+)""")
        for x in diagnostic_basis:
            if x:
                try:
                    entities = ner_api(x)
                    if len(entities) > 0:
                        for entity in entities:
                            if entity['type'] in ['DIS', 'SYM'] and entity['word'] not in ls_value:
                                ls_value.append(entity['word'])
                    # ls_value.append()
                    # entities = [{i['word'] for i in entities if
                    #             i['type'] in ['DIS', 'SYM']]
                    # if len(entities) > 0:
                    #   return entities
                    # else:
                    #   return [{i: 'DIS'} for i in re.split('[， ]', entities)]
                    # ls_value.append(re_item.search(x).group(1))
                except AttributeError:
                    pass
    return ls_value

  def parse_cure_plan(self, text):
    """
    治疗方案
    :param text:
    :return:
    """
    cure_plan = [x.replace("。", '').replace(" ", '') for x in text if x]
    ls_value = []
    if len(cure_plan) > 0:
        for x in cure_plan:
            if x:
                try:
                    entities = ner_api(x)
                    if len(entities) > 0:
                        for entity in entities:
                            if entity['type'] in ['PRP'] and entity['word'] not in ls_value:
                                ls_value.append(entity['word'])
                except AttributeError:
                    pass
    return ls_value

  def parse_examination_items(self, text):
    """
    住院后检查项目
    :param text:
    :return:
    """
    examination_items = [x.replace("。", '').replace(" ", '') for x in text if x]
    ls_value = []
    if len(examination_items) > 0:
        for x in examination_items:
            if x:
                try:
                    entities = ner_api(x)
                    if len(entities) > 0:
                        for entity in entities:
                            if entity['type'] in ['TES'] and entity['word'] not in ls_value:
                                ls_value.append(entity['word'])
                except AttributeError:
                    pass
    return ls_value

  def parse_recommend_drug(self, text):
      """
      用药
      :param text:
      :return:
      """
      ls_recommend_drug = [x.replace("。", '').replace(" ", '') for x in text if x]
      dict_drug = {'drug_category': [], 'drug': []}
      if len(ls_recommend_drug) > 0:
          for recommend_drug in ls_recommend_drug:
              if recommend_drug:
                  try:
                      entities = ner_api(recommend_drug)
                      if len(entities) > 0:
                          for entity in entities:
                              if entity['type'] in ['PRP']:
                                  if entity['word'] not in dict_drug['drug_category'] and entity['word'] != '治疗':
                                      dict_drug['drug_category'].append(entity['word'])
                              if entity['type'] in ['DRU']:
                                  if entity['word'] not in dict_drug['drug'] and entity['word'] != '药物':
                                      dict_drug['drug'].append(entity['word'])
                  except AttributeError:
                      pass
      return dict_drug

  def parse_contraindications_attention(self, text):
      """
      用药禁忌与注意, 如使用禁忌药，则可找出明显异常点。
      :param text:
      :return:
      """
      ls_contraindications_attention = [x.replace("。", '').replace(" ", '') for x in text if x]
      dict_contraindications_attention = {'disease': [],
                                          'sign': [],
                                          'examination': [],
                                          'drug': [],
                                          'symptom': []}
      if len(ls_contraindications_attention) > 0:
          for contraindications_attention in ls_contraindications_attention:
              if contraindications_attention:
                  try:
                      entities = ner_api(contraindications_attention)
                      # newdict = {}
                      # for k, v in [(key, d[key]) for d in entities for key in d]:
                      #   if k not in newdict:
                      #     newdict[k] = [v]
                      #   else:
                      #     newdict[k].append(v)
                      if len(entities) > 0:
                          for entity in entities:
                              if entity['type'] in ['DIS']:
                                  if entity['word'] not in dict_contraindications_attention['disease']:
                                      dict_contraindications_attention['disease'].append(entity['word'])
                              if entity['type'] in ['DRU']:
                                  if entity['word'] not in dict_contraindications_attention['drug'] and entity['word'] not in ['药物', '用药']:
                                      dict_contraindications_attention['drug'].append(entity['word'])
                              if entity['type'] in ['SGN']:
                                  if entity['word'] not in dict_contraindications_attention['sign']:
                                      dict_contraindications_attention['sign'].append(entity['word'])
                              if entity['type'] in ['TES']:
                                  if entity['word'] not in dict_contraindications_attention['examination']:
                                      dict_contraindications_attention['examination'].append(entity['word'])
                              if entity['type'] in ['SYM']:
                                if entity['word'] not in dict_contraindications_attention['symptom']:
                                  dict_contraindications_attention['symptom'].append(entity['word'])
                  except AttributeError:
                      pass
      return dict_contraindications_attention

  def get_batch(self, txt_dict):
    output_dict = {}
    if '入院日期' in txt_dict:
      output_dict['入院日期'] = re.split('[\t\r\n ]', txt_dict['入院日期'])[0]
    try:
      output_dict['入院诊断'] = self.parse_hospital_diagnose(txt_dict['入院诊断'])
    except:
      pass
    try:
      output_dict['出院诊断'] = self.parse_hospital_diagnose(txt_dict['出院诊断'])
    except:
      pass
    try:
      output_dict['出院医嘱'] = self.parse_medical_orders(txt_dict['出院医嘱'])
    except:
      pass
    try:
      output_dict['诊疗经过'] = [{i['word']: i['type']} for i in self.ner_api(txt_dict['诊疗经过']) if
                             i['type'] in ['DRU', 'SGN', 'TES'] and len(i['word']) >= 2]
    except:
      pass
    try:
      output_dict['主诉'] = self.parse_complain(txt_dict['入院情况'])
    except:
      pass
    try:
      output_dict['既往史'] = self.parse_his_dis(txt_dict['入院情况'])
    except:
      pass
    try:
      output_dict['出院情况'] = [{i['word']: i['type']} for i in self.ner_api(txt_dict['出院情况']) if
                             i['type'] in ['DRU', 'SGN', 'TES', 'SYM'] and len(i['word']) >= 2]
    except:
      pass
    try:
      output_dict['入院查体'] = self.parse_physical_examination(txt_dict['入院情况'])
    except:
      pass
    try:
      output_dict['入院情况'] = self.parse_ryqk(txt_dict['入院情况'])
    except:
      pass
    try:
      output_dict['患者信息'] = self.parse_hzxx(txt_dict['患者姓名'])
    except:
      pass
    try:
      output_dict['disease_code'] = self.parse_appliable_target(txt_dict['适用对象'])
    except:
      pass
    try:
      output_dict['症状'] = self.parse_diagnostic_basis(txt_dict['诊断依据'])
    except:
      pass
    try:
      output_dict['治疗'] = self.parse_cure_plan(txt_dict['治疗方案选择依据'])
    except:
      pass
    try:
      output_dict['标准住院日为'] = txt_dict['标准住院日为']
    except:
      pass
    try:
      output_dict['检查项目'] = self.parse_examination_items(txt_dict['住院后检查项目'])
    except:
      pass
    try:
      output_dict['选择用药'] = self.parse_recommend_drug(txt_dict['选择用药'])
    except:
      pass
    try:
      output_dict['禁忌'] = self.parse_contraindications_attention(txt_dict['禁忌证'])
    except:
      pass
    return output_dict

def main():
    # df_clinical_pathway = pd.read_excel('data/临床路径_struct.xlsx', encoding='utf-8')
    with open('./data/test.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    txt_dict = txt_to_json(txt)
    ie = InfoExtr()
    output = ie.get_batch(txt_dict)

    with open('./data/intravenous_thrombolysis.pkl', 'wb') as f:
        pickle.dump(output, f)
    with open('./data/intravenous_thrombolysis.json', 'w') as f:
        file_json = json.dumps(output)
        json.dump(file_json, f)

if __name__ == '__main__':
    main()

def ner_api(text):
    url = 'http://192.168.4.30:5011/NERBegin'
    '''调用实体识别'''
    r = requests.post(url, data={'inputStr': text})
    entities = eval(r.text)[0]['entities']
    return entities