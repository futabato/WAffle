import datetime
import json
import re
import subprocess

from flask import (Flask, Response, escape, make_response, render_template,
                   request)
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

with open("blacklist.txt") as f:
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
    if waf(path, request.get_data().decode(), cookie):
        return render_template('waffle.html')

    try :
        proc = subprocess.run(["curl", "-X", request.method, "-i", "-A", request.user_agent.string, url+path, "-H", "Cookie: " + cookie, "-H", "Content-Type:" + request.headers.getlist("Content-Type")[0] , "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        proc = subprocess.run(["curl", "-X", request.method, "-i", "-A", request.user_agent.string, url+path, "-H", "Cookie: " + cookie, "-H", "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # HTTPリクエストをヘッダとボディで分割
    splited_res = proc.stdout.split("\r\n\r\n".encode("utf-8"),1)
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

def waf(path, body, cookie):
    msg = ""
    for val in blacklist:
        m = re.match(val, path, re.IGNORECASE)
        if m == None and body != "":
            m = re.match(val, str(body), re.IGNORECASE)
        if m == None and cookie != "":
            m = re.match(val, str(cookie), re.IGNORECASE)
            
        msg = str({"date": str(datetime.datetime.now()), "path": str(escape(path)), "body": str(escape(body)), "cookie": str(escape(cookie))}) + "\n"
        if m != None:
            with open('log/block.txt', mode='a') as f:
                f.write(msg)
            return True
    with open('log/through.txt', mode='a') as f:
        f.write(msg)
    return False

app.run()
