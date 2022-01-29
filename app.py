from flask import Flask, render_template, request, g
import sys
import sqlite3 as sql

sys.path.append("./lstm")
from serve import *

app = Flask(__name__)


DATABASE = "CommentData.db"


def connect_db():
    return sql.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [
        dict((cur.description[idx][0], value) for idx, value in enumerate(row))
        for row in cur.fetchall()
    ]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


@app.route("/")
def home():
    ret = []
    for data in query_db("select * from CommentData ORDER BY RANDOM() limit 5"):
        ret.append(data)
        print(ret)
    return render_template("home.html", data=ret)


@app.route("/test")
def student():
    return render_template("Test.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        print("=========================")
        print(f"input={request.form.get('InputText')}")
        input = request.form.get("InputText")
        res = {"InputText": input, "result": SingleTest(input)}
        print("=========================")
        return render_template("result.html", result=res)
    else:
        print(request.method)
        print(f"input={request.form.get('InputText')}")
        return render_template("result.html", result={"res": "ERROR"})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
