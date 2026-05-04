#!/usr/bin/env python

import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * 20
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT tweets.text, tweets.created_at, users.screen_name
        FROM tweets
        JOIN users ON tweets.id_users = users.id_users
        ORDER BY tweets.created_at DESC
        LIMIT 20 OFFSET %s
    """, (offset,))
    tweets = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tweets=tweets, page=page)
