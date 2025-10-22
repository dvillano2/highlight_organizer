from typing import Dict
from typing import List
from typing import Tuple
import re
import sqlite3
from patterns import team_regex
from youtube_urls import pull_possible_video_urls


def filter_for_highlights(video_info: list[dict]) -> list[dict]:
    "drop videos that don't have highlights in their title"
    return [
        info for info in video_info if "highlights" in info["title"].lower()
    ]


def format_date_for_displayed_comparison(date: str) -> str:
    "massage dates into the form NBC sports displays them on their channel"
    no_time: str = date.split(" ")[0]
    reordered: str = no_time[5:7] + "/" + no_time[-2:] + "/" + no_time[:4]
    if reordered[3] == "0":
        reordered = reordered[:3] + reordered[4:]
    if reordered[0] == "0":
        reordered = reordered[1:]
    return reordered


def pull_finished_games():
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT full_date, home, away, id FROM schedule "
        "WHERE finished = 'yes' AND youtube_url = '';"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def format_games(
    games_info: List[Tuple[str, str, str, str]]
) -> List[Tuple[re.Pattern, re.Pattern, re.Pattern, str]]:
    "assumes games info comes from a select full_date, home, away ,id query"
    regex = {
        team_name: re.compile(team_regex_pattern, re.IGNORECASE)
        for team_name, team_regex_pattern in team_regex().items()
    }
    return [
        (
            re.compile(format_date_for_displayed_comparison(game[0])),
            regex[game[1]],
            regex[game[2]],
            game[3],
        )
        for game in games_info
    ]


def match_games_to_videos(
    video_info: List[Dict],
    games_info: List[Tuple[str, str, str, str]],
) -> Tuple[List[Tuple[str, str]], List[str]]:
    """
    this is naive with the double loop, various ways to make it better
    but everything is so small that it doesn't really matter
    still, better to sort by date desending in the query
    """
    formatted_games = format_games(games_info)
    url_id: List[Tuple[str, str]] = []
    missed_games = []
    for game in formatted_games:
        game_id = game[3]
        matching_items = game[:3]
        for video in video_info:
            missed = True
            if all(
                pattern.search(video["title"]) for pattern in matching_items
            ):
                url_id.append((video["url"], game_id))
                missed = False
                break
        if missed:
            missed_games.append(game_id)
    return url_id, missed_games


def update_db_with_links(url_id_pairs: List[Tuple[str, str]]) -> None:
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.executemany(
        "UPDATE schedule SET youtube_url = ? WHERE id = ?;", url_id_pairs
    )
    conn.commit()
    cursor.close()
    conn.close()
    return


def update_missing_links():
    possible_videos = pull_possible_video_urls()
    highlight_videos = filter_for_highlights(possible_videos)
    games = pull_finished_games()
    url_id, missing_games = match_games_to_videos(highlight_videos, games)
    update_db_with_links(url_id)
    return missing_games
