import datetime
import re

import requests
from flask import Flask, Response, render_template
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

f = open('log/block.txt','w')
f.write('')
f.close()
f = open('log/through.txt','w')
f.write('')
f.close()

@app.route('/<regex(".*"):path>')
def proxy(path):

    for val in blacklist:
        m = re.match(val, path, re.IGNORECASE)
        if m != None :
            with open('log/block.txt', mode='a') as f:
                f.write("[" + str(datetime.datetime.now()) + "] " + path + '\n')
            return render_template('waffle.html')    

    with open('log/through.txt', mode='a') as f:
        f.write("[" + str(datetime.datetime.now()) + "] " + path + '\n')
    url = "http://localhost:80/"+path
    r = requests.get(url)
    return Response(r.content)

app.run()
