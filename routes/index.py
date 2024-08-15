from flask import Flask, Blueprint
import sqlite3

from consts import DATABASE

app = Blueprint('index', __name__)
@app.route("/")
def root():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM token WHERE value = "2yl8Tub9qfLaRZOij02Y"')
    records = cursor.fetchone()
    conn.close
    # print(str(records[0]))
    # print("asd", flush=True)
    return str(records[0])  # user id
    # return "hello, world"
