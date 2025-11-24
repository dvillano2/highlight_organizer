from pull_info import make_dict, pull_db_info
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    rows = pull_db_info()
    highlights = make_dict(rows)
    return render_template("highlights.html", highlights=highlights)
