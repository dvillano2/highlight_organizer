"""Organizes official PL website which is hardcoded in the first function"""

import json
import sqlite3
from datetime import datetime
from typing import Dict
from typing import Tuple
from typing import Union
from io import StringIO
import pandas as pd
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
        "full_date": date_obj.strftime("%Y-%m-%d %H:%M"),
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
            "full_date": date_time_info["full_date"],
            "season": season,
            "timezone": match["kickoffTimezone"],
            "id": match["matchId"],
            "finished": "yes" if match["period"] == "FullTime" else "no",
            "youtube_url": "",
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
        }
        counter += 1
    return matches, counter


def pull_single_mw(
    mw: int, base_url: str = mw_url_base(), counter: int = 1, concat=False
) -> Union[Tuple[Dict[int, Dict[str, str]], int], Dict[int, Dict[str, str]]]:
    url = base_url + str(mw)
    response = requests.get(url)
    mw_dict = json.loads(response.text)
    matches, counter = organize_single_mw(mw_dict, counter)
    if concat:
        return matches, counter
    return matches


def organize_mws(min_mw=1) -> Dict[int, Dict[str, str]]:
    """For 2025-2026 season"""
    base_url = mw_url_base()
    mws: Dict = {}
    counter = 1
    for mw in range(min_mw, 39):
        matches, counter = pull_single_mw(mw, base_url, counter, True)
        assert isinstance(matches, dict)
        mws |= matches
    return mws


def mws_to_df(mws: Dict[int, Dict[str, str]]) -> pd.DataFrame:
    """Makes the mws dict a df"""
    mws_json = json.dumps(mws)
    df = pd.read_json(StringIO(mws_json))
    return df.T


def main() -> None:
    """Writes the schedule to a tiny db"""
    mws = organize_mws()
    df = mws_to_df(mws)
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS schedule;")
    cursor.close()
    conn.commit()
    df.to_sql(
        "schedule",
        conn,
        index=False,
        dtype={"mw": "INTEGER", "id": "TEXT PRIMARY KEY"},
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
