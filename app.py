import os
import sqlite3
import datetime

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from flask_htmx import HTMX
from flask_htmx import make_response

app = Flask(__name__)
htmx = HTMX(app)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/messages", methods=["GET"])
def message():
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM message").fetchall()
    conn.close()

    tmpl = """
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
    """
    body = [tmpl.format(m["person"], m["text"], m["created"]) for m in messages]
    resp = "".join(body)

    return make_response(resp, push_url=False)


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    message = request.form.get("message")
    timestamp = str(datetime.datetime.now())

    if name and message:
        print(f"Request for hello page received with name={name} and message={message}")

        conn = get_db_connection()
        conn.execute(
            f"INSERT INTO message (person, text, created) VALUES ('{name}', '{message}', '{timestamp}')"
        )
        conn.commit()
        conn.close()

        resp = f"""
        <tr>
            <td>{name}</td>
            <td>{message}</td>
            <td>{timestamp}</td>
        </tr>
        """

        return make_response(resp, push_url=False)
    else:
        print("error")
        return None


if __name__ == "__main__":
    app.run()
