import re
from patterns import mw_regex
from patterns import day_num_regex
from patterns import month_regex

MWREGEX = mw_regex()
DAYNUMREGEX = day_num_regex()
MONTHREGEX = month_regex()


def match_mw(text):
    search = re.search(MWREGEX, text, re.I)
    if search:
        match = search.group(0)
        return re.search(r"\d\d?", match).group(0)
    return None

def match_day_num(text):
    search = re.search(DAYNUMREGEX, text, re.I)
    if search:
        match = search.group(0)
        day_num = match.split(" ")
        return {"day": day_num[0], "num": day_num[1]}
    return {"day": None, "num": None}

def match_month(text):
    search = re.search(MONTHREGEX, text, re.I)
    if search:
        match = search.group(0)
        return match
    return None

def check_line(line):
    tracker = {}
    tracker['mw'] = match_mw(line)
    tracker["month" ] = match_month(line)
    day_num = match_day_num(line)
    tracker["day"] = day_num["day"]
    tracker["num"] = day_num["num"]
    return tracker

def organize(info_nop):
    matchweek = None
    day_of_week = None
    day = None
    month = None
    year = None
    for line in info_nop:

