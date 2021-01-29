import datetime
import json
from os import write
import re
import subprocess
import urllib.parse

from flask import (Flask, Response, escape, make_response, render_template,
                   request)
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
    blacklist = [s.strip() for s in f.readlines()]

# 2つのログファイルを初期化
f = open('log/block.txt', 'w')
f.write('')
f.close()
f = open('log/through.txt', 'w')
f.write('')
f.close()

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

    # WAF
    """イメージ
    def post():
        if signature():
            return render_template('waffle.html')
        elif predict():
            return render_template('waffle.html')
    """


    confidence_score = waf(url, path, str(escape((request.get_data()).decode('utf-8'))), str(escape(cookie)))
    msg = str({"date": str(datetime.datetime.now()), "ip": request.remote_addr,"path": str(escape(path)), "body": str(escape((request.get_data()).decode('utf-8'))), "cookie": str(escape(cookie)), "confidence_score":confidence_score}) + "\n"
    if confidence_score > 0.8:
        with open('log/block.txt', 'a') as f:
            f.write(msg)
        return render_template('waffle.html')
    else :
        with open('log/through.txt', 'a') as f:
            f.write(msg)

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
        return 1
    confidence_score = prediction(url + path)
    # ここのしきい値は適切に判断する必要がある(0.8は高いけどPrecisionを高くしたくない)
    return confidence_score

# 定義済みのシグネチャを参照したパターンマッチング
def signature(path, body, cookie):
    for val in blacklist:
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
    input_url = np.array([UNICODE_encoded_url])
    return input_url

# 機械学習を使った推論処理
def prediction(url):    
    # セッションのクリア(必要なのかは不明ではある)
    K.clear_session()
    model = load_model('../model/model.h5')

    input_url = preprocess(url)
    result = model.predict(input_url)
    confidence_score = result[0][0]
    
    #print('url: ', url)
    #print('confidence-score: ', confidence_score)
    # msg = str({"url": url, "confidence_score": str(confidence_score),}) + "\n"
    return confidence_score

app.run("0.0.0.0")
