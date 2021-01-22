import datetime
import json
import re
import subprocess

from flask import Flask, Response, render_template, request
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
    query = request.query_string
    if query != b'' :
        path += "?" + query.decode()

    if waf(request.remote_addr, path, request.get_data().decode()):
        return render_template('waffle.html')

    try :
        proc = subprocess.run(["curl", "-X", request.method, "-A", request.user_agent.string, url+path,"-H","Content-Type:" + request.headers.getlist("Content-Type")[0] , "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        proc = subprocess.run(["curl", "-X", request.method, "-A", request.user_agent.string, url+path, "--data", request.get_data().decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return Response(proc.stdout)

def waf(addr, path, body):
    for val in blacklist:
        m = re.match(val, path, re.IGNORECASE)
        if m == None and body != "":
            m = re.match(val, str(body), re.IGNORECASE)
            
        if m != None:
            with open('log/block.txt', mode='a') as f:
                f.write(str({"date": str(datetime.datetime.now()), "ip": addr, "path": path, "body": body}) + "\n")
            return True
    with open('log/through.txt', mode='a') as f:
        f.write(str({"date": str(datetime.datetime.now()), "ip": addr, "path": path, "body": body}) + "\n")
    return False

app.run()
