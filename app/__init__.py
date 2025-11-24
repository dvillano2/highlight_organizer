import time
from .pull_info import make_dict, pull_db_info
from flask import Flask, render_template

app = Flask(__name__)


cache = {"highlights": None, "last_access": 0}

CACHE_TTL = 60


@app.route("/")
def home():
    now = time.time()
    if cache["highlights"] is None or now - cache["last_access"] > CACHE_TTL:
        rows = pull_db_info()
        cache["highlights"] = make_dict(rows)
        cache["last_access"] = now
    return render_template("highlights.html", highlights=cache["highlights"])
