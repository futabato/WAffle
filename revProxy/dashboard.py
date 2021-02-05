import re

from flask import Flask, Markup, render_template, request

app = Flask(__name__)

@app.route('/')
def dashboard():
    with open("log/block.txt") as f:
        block_list = [s.strip() for s in f.readlines()]
    with open("log/through.txt") as f:
        through_list = [s.strip() for s in f.readlines()]
    return render_template('dashboard.html', block_len=len(block_list), through_len=len(through_list))

@app.route('/log', methods=["GET", "POST"])
def log():
    if request.method == "GET":
        with open("log/block.txt") as f:
            block_list = [s.strip() for s in f.readlines()]
        with open("log/through.txt") as f:
            through_list = [s.strip() for s in f.readlines()]
        return render_template('logs.html', block_req=",".join(block_list), through_req=",".join(through_list))
    return None

app.run(port=5001)
