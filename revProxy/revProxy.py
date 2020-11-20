import datetime
import re
import subprocess

import requests
from flask import Flask, Response, render_template
from flask import request as req
from requests.api import request
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

with open("blacklist.txt") as f:
    blacklist = [s.strip() for s in f.readlines()]

f = open('log/block.txt', 'w')
f.write('')
f.close()
f = open('log/through.txt', 'w')
f.write('')
f.close()

url = "http://localhost:8080/"

@app.route('/<regex(".*"):path>', methods=["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
def post(path):
    query = req.query_string
    if query != b'' :
        path += "?" + query.decode()

    if waf(path, req.get_data().decode()):
        return render_template('waffle.html')

    try :
        proc = subprocess.run(["curl", "-X", req.method, url+path,"-H","Content-Type:" + req.headers.getlist("Content-Type")[0] , "--data", req.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        proc = subprocess.run(["curl", "-X", req.method, url+path, "--data", req.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return Response(proc.stdout)

def waf(path, *body):
    for val in blacklist:
        m = re.match(val, path, re.IGNORECASE)
        if m == None and body != ():
            m = re.match(val, str(body), re.IGNORECASE)
            
        if m != None:
            with open('log/block.txt', mode='a') as f:
                f.write("[" + str(datetime.datetime.now()) + "] " + path + " " + str(body) +"\n")
            return True
    with open('log/through.txt', mode='a') as f:
        f.write("[" + str(datetime.datetime.now()) + "] " + path + " " + str(body) + "\n")
    return False

app.run()
