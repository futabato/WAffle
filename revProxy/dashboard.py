import re

import requests
from flask import Flask, render_template
from requests.api import request

app = Flask(__name__)

@app.route('/')
def dashboard():
    with open("log/block.txt") as f:
        block_list = [s.strip() for s in f.readlines()]
    with open("log/through.txt") as f:
        through_list = [s.strip() for s in f.readlines()]
    return render_template('dashboard.html', block_len=len(block_list), through_len=len(through_list))

@app.route('/log')
def log():
    with open("log/block.txt") as f:
        block_list = [s.strip() for s in f.readlines()]
    with open("log/through.txt") as f:
        through_list = [s.strip() for s in f.readlines()]
    return render_template('logs.html', block_req=block_list, through_req=through_list)


app.run(port=5001)
