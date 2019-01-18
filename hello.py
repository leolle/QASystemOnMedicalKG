from gevent import pywsgi, monkey
monkey.patch_all()
from flask import Flask, request
import json, time, datetime, os
import pandas as pd
import numpy as np
import tensorflow as tf
import traceback
import logging
from lib_zhou.utils import get_logger2
import predict_a, predict_b, predict_c

def str2date(s, sep='-'):
    return datetime.datetime.strptime(s, "%Y-%m-%d")

def producer(test_data, input_dis):
    d2 = pd.DataFrame(test_data['sequence'])
    d2.rename(columns={'patientId': 'PERSON_ID',
                       'timeLine': 'TIME_LINE',
                       'diagnoseCode': 'DIAGNOSE_CODE',
                       'drugCode': 'DRUG_CODE',
                       'proceCode': 'PROCEDURE_CODE',
                       'labId': "LABORATORY_ID",
                       'labValue': "LABORATORY_VALUE",
                       'labAssess': "LABORATORY_ASSESS",
                       'age': "AGE"
                       },
              inplace=True
              )
    if "AGE" not in d2:
        d2['AGE'] = d2['TIME_LINE'].map(
            lambda x: (str2date(x) - str2date(test_data['birthDate'])).days)
    if 'PERSON_ID' not in d2:
        d2['PERSON_ID'] = test_data['patientId']
    test_data.pop('sequence')
    d1 = pd.DataFrame(
        [
            [test_data['patientId'], test_data['name'], test_data['age'], test_data['sex'],
             test_data['job'], test_data['maritalStatus'], test_data['smoking'],
             test_data['famiHistory'], test_data['selfHistory'],
             test_data['abnormLab'],
             ]
        ],
        columns=['ID', 'NAME', 'AGE', 'SEX', 'JOB', 'MARITAL_STATUS', 'SMOKING',
                 'FAMILY_HISTORY', 'SELF_HISTORY', 'ABNORM_LAB'])

    r = {}
    if input_dis.strip() == '2':
        r = predict_b.get_risk_infos(test_data['patientId'], d1, d2)
    elif input_dis == '3':
        r = predict_c.get_risk_infos(test_data['patientId'], d1, d2)
    else:
        r = predict_a.get_risk_infos(test_data['patientId'], d1, d2)

    return r

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<p><a href="./risk">º≤≤°∑Áœ’‘§≤‚“˝«Ê</a></p>'


@app.route('/risk', methods=['GET'])
def signin_form():
    return '''<body><form action="/risk" method="post">
                <!-- <p><input name="input" placeholder="input" size="180"></p> -->
                <textarea name="input" placeholder="input" clos=",50" cols="180" rows="20" warp="virtual"></textarea>
                <p><input name="disease" placeholder="disease" size="20"></p>
                <p><button type="submit">OK</button></p>
            </form>
            </body>'''


@app.route('/risk', methods=['POST'])
def signin():
    input_json = request.form['input']
    input_dis = request.form['disease']
    try:
        result = json.dumps(producer(json.loads(input_json), input_dis),
                            ensure_ascii=False)
    except:
        result = 'Fault'
        logger.info(traceback.format_exc())
    return result

if __name__ == '__main__':
    host, port = '0.0.0.0', 5277
    s = "* Running on http://{}:{}/".format(host, port)
    pywsgi.WSGIServer((host, port), app).serve_forever()
