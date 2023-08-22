import os
import sqlite3

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    people = conn.execute("SELECT * FROM people").fetchall()
    conn.close()
    print("Request for index page received")
    return render_template("index.html", people=people)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")

    if name:
        print("Request for hello page received with name=%s" % name)

        conn = get_db_connection()
        people = conn.execute(f"INSERT INTO people (person) VALUES ('{name}')")
        conn.commit()
        conn.close()

        return render_template("hello.html", name=name)
    else:
        print(
            "Request for hello page received with no name or blank name -- redirecting"
        )
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
