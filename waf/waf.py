import datetime
import json
from os import write
import re
import subprocess
import urllib.parse
import csv

from flask import (Flask, Response, escape, make_response, render_template, request)
from werkzeug.routing import BaseConverter
import numpy as np
from keras.models import load_model
from keras import backend as K

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

with open("denylist.txt") as f:
    denylist = [s.strip() for s in f.readlines()]

# 4つのログファイルを初期化
with open('log/block.txt', 'w') as block_txt:
    block_txt.write('')
with open('log/through.txt', 'w') as through_txt:
    through_txt.write('')
with open('../analysis/block.csv', 'w', newline='') as block_csv:
    block_writer = csv.writer(block_csv)
    block_writer.writerow(['date', 'ip', 'path', 'body', 'cookie', 'is_abnormal'])
with open('../analysis/through.csv', 'w', newline='') as through_csv:
    through_writer = csv.writer(through_csv)
    through_writer.writerow(['date', 'ip', 'path', 'body', 'cookie', 'is_abnormal'])

# 保護対象のURL
url = "http://localhost:8080/"

@app.route('/<regex(".*"):path>', methods=["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
def post(path):
    # URLクエリを抽出
    query = request.query_string
    if query != b'' :
        path += "?" + query.decode()

    # cookieを抽出
    cookie = ""
    for i ,v in request.cookies.items():
        cookie += i + "=" + v +";"

    # リクエストデータの整理
    date_data = datetime.datetime.now()
    ip_data = request.remote_addr
    path_data = escape(path)
    body_data = escape((request.get_data()).decode('UTF-8'))
    cookie_data = escape(cookie)

    # パターンマッチと機械学習で悪意ある通信を遮断
    is_abnormal = waf(url, path, str(body_data), str(cookie_data))
    msg_txt = str({"date": str(date_data), "ip": ip_data,"path": str(path_data), "body": str(body_data), "cookie": str(cookie_data), "is_abnormal": is_abnormal}) + "\n"

    # (汎化性能皆無のため)vuln利用時、推論処理を避けるために is_abnormal==1 にしています
    if is_abnormal == 1:
        with open('log/block.txt', 'a') as block_txt:
            block_txt.write(msg_txt)
        with open('../analysis/block.csv', 'a', newline='') as block_csv:
            block_writer = csv.writer(block_csv)
            block_writer.writerow([date_data, str(ip_data), path_data, body_data, cookie_data, is_abnormal])
        return render_template('waffle.html')
    else :
        with open('log/through.txt', 'a') as through_txt:
            through_txt.write(msg_txt)
        with open('../analysis/through.csv', 'a', newline='') as through_csv:
            through_writer = csv.writer(through_csv)
            through_writer.writerow([date_data, str(ip_data), path_data, body_data, cookie_data, is_abnormal])
    try :
        proc = subprocess.run(["curl", "-X", request.method, "-i", "-A", request.user_agent.string, url+path, "-H", "Cookie: " + cookie, "-H", "Content-Type:" + request.headers.getlist("Content-Type")[0] , "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        proc = subprocess.run(["curl", "-X", request.method, "-i", "-A", request.user_agent.string, url+path, "-H", "Cookie: " + cookie, "-H", "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # HTTPリクエストをヘッダとボディで分割
    splited_res = proc.stdout.split("\r\n\r\n".encode("utf-8"), 1)
    if len(splited_res) == 1:
        res = make_response("")
    else :
        res = make_response(splited_res[1])

    # HTTPリクエストヘッダからcookieを探してセットする
    for v in splited_res[0].split("\r\n".encode("utf-8")):
        if v.startswith(b'Set-Cookie'):
            s = v.split(":".encode("utf-8"), 1)[1].split("=".encode("utf-8"), 1)
            res.set_cookie(s[0].decode("utf-8"), s[1].split(";".encode("utf-8"), 1)[0].decode('utf-8'))

    return res

def waf(url, path, body, cookie):
    if not signature(path, body, cookie):
        # パターンマッチングで引っかかった場合100%異常とする
        return 1
    else:
        return prediction(url + path)

# 定義済みのシグネチャを参照したパターンマッチング
def signature(path, body, cookie):
    for val in denylist:
        m = re.match(val, path, re.IGNORECASE)
        if m == None and body != "":
            m = re.match(val, str(body), re.IGNORECASE)
        if m == None and cookie != "":
            m = re.match(val, str(cookie), re.IGNORECASE)
        if m != None :
            return False
    return True

# 前処理
def preprocess(url):
    # url decode
    URL_decoded_url = urllib.parse.unquote(url)
    URL_decoded_url = [s.lower() for s in URL_decoded_url]
    # unicode encode
    UNICODE_encoded_url = [ord(x) for x in str(URL_decoded_url).strip()]
    UNICODE_encoded_url = UNICODE_encoded_url[:1000]
    # zero padding
    if len(UNICODE_encoded_url) <= 1000:
        UNICODE_encoded_url += ([0] * (1000 - len(UNICODE_encoded_url)))
    # convert to numpy array
    model_input_url = np.array([UNICODE_encoded_url])
    return model_input_url

# 機械学習を使った推論処理
def prediction(url):    
    # セッションのクリア(必要なのかは不明ではある)
    K.clear_session()
    model = load_model('../model/model.h5')

    model_input_url = preprocess(url)
    result = model.predict(model_input_url)
    return result[0][0]

app.run("0.0.0.0")
