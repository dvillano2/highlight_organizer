from typing import Dict
from typing import List


def filter_for_highlights(video_info: list[dict]) -> list[dict]:
    return [
        info for info in video_info if "highlights" in info["title"].lower()
    ]


def format_date_for_displayed_comparison(date: str) -> str:
    no_time: str = date.split(" ")[0]
    reordered: str = no_time[5:7] + "/" + no_time[-2:] + "/" + no_time[:4]
    if reordered[3] == "0":
        reordered = reordered[:3] + reordered[4:]
    if reordered[0] == "0":
        reordered = reordered[1:]
    return reordered


def match_dates(video_info: List[Dict], dates: list) -> List[Dict]:
    formatted_dates = [filter_for_highlights(date) for date in dates]
    return [
        info
        for info in video_info
        if any(date in info["title"] for date in formatted_dates)
    ]
