#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Date: 18-10-4
from gevent import pywsgi, monkey
monkey.patch_all()
from flask import Flask, request
import json
import traceback
from question_classifier import *
from question_parser import *
from answer_search import *
from ylog import *


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是医疗智能助理小琦，请输入您的问题或者描述，希望可以帮到您。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


handler = ChatBotGraph()
set_level(logging.DEBUG)
console_on()
filelog_on("app")
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<p><a href="./chatbot">疾病风险预测引擎</a></p>'


@app.route('/chatbot', methods=['GET'])
def signin_form():
    return '''<body><form action="/chatbot" method="post">
                <!-- <p><input name="input" placeholder="input" size="180"></p> -->
                <textarea name="input" placeholder="input" clos=",50" cols="180" rows="20" warp="virtual"></textarea>
                
                <p><button type="submit">OK</button></p>
            </form>
            </body>'''


@app.route('/chatbot', methods=['POST'])
def signin():
    input_txt = request.form['input']
    # handler = ChatBotGraph()
    try:
        debug(input_txt)
        answer = handler.chat_main(input_txt)
    except:
        answer = '抱歉没找到相关信息，请返回重新输入。'
        debug(traceback.format_exc())
    # print('小琦:', answer)
    # input_dis = request.form['disease']
    # try:
    #     result = json.dumps(producer(json.loads(input_json), input_dis),
    #                         ensure_ascii=False)
    # except:
    #     result = 'Fault'
    #     logger.info(traceback.format_exc())
    return answer



#
# @app.route("/")
# def main():
#     handler = ChatBotGraph()
#     while True:
#         try:
#             question = input('用户:')
#         except UnicodeDecodeError:
#             print('输入有误，请重新输入。')
#         if question:
#             answer = handler.chat_main(question)
#             print('小琦:', answer)


if __name__ == '__main__':
    host, port = '0.0.0.0', 5277
    s = "* Running on http://{}:{}/".format(host, port)
    pywsgi.WSGIServer((host, port), app).serve_forever()
