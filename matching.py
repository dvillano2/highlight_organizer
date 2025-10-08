import re
import json
from patterns import mw_regex
from patterns import day_num_regex
from patterns import month_regex
from patterns import team_regex
from patterns import time_regex
from typing import Dict
from datetime import datetime
from parse_official import get_response
from parse_official import parse_by_mw_respone

MWREGEX = mw_regex()
DAYNUMREGEX = day_num_regex()
MONTHREGEX = month_regex()
TEAMREGEX = team_regex()
TIMEREGEX = time_regex()


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


def match_time(text):
    search = re.search(TIMEREGEX, text)
    if search:
        match = search.group(0)
        return re.search(r"\d\d?\:\d\d", match).group(0)
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
    tracker["time"] = match_time(line)
    day_num = match_day_num(line)
    tracker["day"] = day_num["day"]
    tracker["num"] = day_num["num"]
    teams = check_teams(line)
    tracker["home"] = teams["home"]
    tracker["away"] = teams["away"]
    return tracker


def organize(info, season: str = "2025-2026"):
    matches = {}
    counter = 1
    mw = None
    day = None
    num = None
    month = None
    year = None
    for line in info:
        time = None
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

        line_time = line_info["time"]
        if line_time is not None:
            time = line_time

        if line_info["home"] is not None and line_info["away"] is not None:
            matches[counter] = {
                "mw": mw,
                "day": day,
                "num": num,
                "month": month,
                "time": time,
                "year": year,
                "home": line_info["home"],
                "away": line_info["away"],
                "season": season,
                "timezone": None,
            }
            counter += 1
    return matches


def pull_date_time_data(date_time_str: str):
    date_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    return {
        "year": date_obj.strftime("%Y"),
        "month": date_obj.strftime("%B"),
        "num": date_obj.strftime("%d"),
        "day": date_obj.strftime("%A"),
        "time": date_obj.strftime("%H:%M"),
    }


def by_mw_organize_single(
    mw_info: Dict, counter: int = 1, season: str = "2025-2026"
):
    matches = {}
    for match in mw_info["data"]:
        date_time_info = pull_date_time_data(match["kickoff"])
        matches[counter] = {
            "mw": str(match["matchWeek"]),
            "day": date_time_info["day"],
            "num": date_time_info["num"],
            "month": date_time_info["month"],
            "time": date_time_info["time"],
            "year": date_time_info["year"],
            "season": season,
            "timezone": match["kickoffTimezone"],
            "id": match["matchId"],
            "finished": "yes" if match["period"] == "FullTime" else "no",
            "youtube_link": "",
        }
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        for team in TEAMREGEX.values():
            if re.search(team["regex"], home, re.I) is not None:
                matches[counter]["home"] = team["name"]
            if re.search(team["regex"], away, re.I) is not None:
                matches[counter]["away"] = team["name"]
        counter += 1
    return matches, counter


def by_mw_organize_season(season: str = "2025-2026"):
    with open("schedule_urls.json", "r", encoding="utf-8") as f:
        urls = json.load(f)
    full_season: Dict = {}
    counter = 1
    for mw in range(1, 39):
        response = get_response("mw", urls, mw)
        mw_dict = parse_by_mw_respone(response)
        matches, counter = by_mw_organize_single(mw_dict, counter)
        full_season |= matches
    return full_season
