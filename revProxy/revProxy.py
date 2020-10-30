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
    bList = [s.strip() for s in f.readlines()]

@app.route('/<regex(".*"):path>')
def proxy(path):

    for val in bList:
        m = re.match(val, path, re.IGNORECASE)
        if m != None :
            return render_template('waffle.html')    

    url = "http://localhost:80/"+path
    r = requests.get(url)
    return Response(r.content)

app.run()
