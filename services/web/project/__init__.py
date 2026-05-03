#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Twitter clone coming soon", 200
