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

@app.route('/<regex(".*"):path>')
def proxy(path):
    if "<" in path:
        print(path)
        return render_template('waffle.html')
    url = "http://localhost:80/"+path
    r = requests.get(url)
    return Response(r.content)

app.run()
