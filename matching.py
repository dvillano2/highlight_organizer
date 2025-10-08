import re
from patterns import mw_regex
from patterns import day_num_regex
from patterns import month_regex
from patterns import team_regex

MWREGEX = mw_regex()
DAYNUMREGEX = day_num_regex()
MONTHREGEX = month_regex()
TEAMREGEX = team_regex()


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
        if len(day_num) == 2:
            return {"day": day_num[0], "num": day_num[1]}
    return {"day": None, "num": None}


def match_month(text):
    search = re.search(MONTHREGEX, text, re.I)
    if search:
        match = search.group(0)
        return match
    return None


def check_teams(text):
    v_split = text.split(" v ")
    teams = {"home": None, "away": None}
    if len(v_split) != 2:
        return teams
    for team in TEAMREGEX.values():
        if re.search(team["regex"], v_split[0], re.I) is not None:
            teams["home"] = team["name"]
        if re.search(team["regex"], v_split[1], re.I) is not None:
            teams["away"] = team["name"]
    return teams


def check_line(line):
    tracker = {}
    tracker["mw"] = match_mw(line)
    tracker["month"] = match_month(line)
    day_num = match_day_num(line)
    tracker["day"] = day_num["day"]
    tracker["num"] = day_num["num"]
    teams = check_teams(line)
    tracker["home"] = teams["home"]
    tracker["away"] = teams["away"]
    return tracker


def organize(info):
    matches = {}
    counter = 1
    mw = None
    day = None
    num = None
    month = None
    year = None
    for line in info:
        line_info = check_line(line)
        line_mw = line_info["mw"]
        if line_mw is not None:
            mw = line_mw

        line_month = line_info["month"]
        if line_month is not None:
            month = line_month
            if month in [
                "August",
                "September",
                "October",
                "November",
                "December",
            ]:
                year = "2025"
            else:
                year = "2026"

        line_num = line_info["num"]
        if line_num is not None:
            num = line_num

        line_day = line_info["day"]
        if line_day is not None:
            day = line_day

        if line_info["home"] is not None and line_info["away"] is not None:
            matches[counter] = {
                "mw": mw,
                "day": day,
                "num": num,
                "month": month,
                "year": year,
                "home": line_info["home"],
                "away": line_info["away"],
            }
            counter += 1
    return matches
