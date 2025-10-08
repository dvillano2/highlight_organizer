"""Urls to pull schedule info, multiples so the corroborate each other"""

from typing import Dict
from typing import Union
import json


def mw_url_base() -> str:
    return (
        "https://sdp-prem-prod.premier-league-prod.pulselive.com/"
        "api/v2/matches?competition=8&season=2025&matchweek="
    )


def season_start_url() -> str:
    return (
        "https://sdp-prem-prod.premier-league-prod.pulselive.com"
        "/api/v2/matches?competition=8&season=2025&matchweek="
    )


def make_mw_urls() -> Dict[str, str]:
    base: str = mw_url_base()
    mw_urls: Dict[str, str] = {}
    for i in range(1, 39):
        mw_index = str(i)
        mw_urls[mw_index] = base + mw_index
    return mw_urls


def make_2526_urls() -> Dict[str, Union[str, Dict[str, str]]]:
    urls: Dict[str, Union[str, Dict[str, str]]] = {}
    urls["by_mw"] = make_mw_urls()
    urls["season_start"] = season_start_url()
    return urls


def main() -> None:
    schedule_urls = make_2526_urls()
    with open("schedule_urls.json", "w", encoding="utf-8") as f:
        json.dump(schedule_urls, f, indent=4)


if __name__ == "__main__":
    main()
