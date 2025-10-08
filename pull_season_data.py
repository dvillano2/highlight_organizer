"""Organizes official PL website which is hardcoded in the first function"""

import json
from datetime import datetime
from typing import Dict
from typing import Tuple
import requests


def mw_url_base() -> str:
    "Hardcoded base url for pulling mw info"
    return (
        "https://sdp-prem-prod.premier-league-prod.pulselive.com/"
        "api/v2/matches?competition=8&season=2025&matchweek="
    )


def pull_date_time_data(date_time_str: str) -> Dict[str, str]:
    "Helper for parsing date and time info"
    date_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    return {
        "year": date_obj.strftime("%Y"),
        "month": date_obj.strftime("%B"),
        "num": date_obj.strftime("%d"),
        "day": date_obj.strftime("%A"),
        "time": date_obj.strftime("%H:%M"),
    }


def organize_single_mw(
    mw_info: Dict, counter: int = 1, season: str = "2025-2026"
) -> Tuple[Dict[int, Dict[str, str]], int]:
    """Organizes a single matchweek"""
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
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
        }
        counter += 1
    return matches, counter


def organize_season() -> Dict[int, Dict[str, str]]:
    """For 2025-2026 season"""
    base_url = mw_url_base()
    full_season: Dict = {}
    counter = 1
    for mw in range(1, 39):
        url = base_url + str(mw)
        response = requests.get(url)
        mw_dict = json.loads(response.text)
        matches, counter = organize_single_mw(mw_dict, counter)
        full_season |= matches
    return full_season
