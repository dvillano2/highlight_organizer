"""Main funciton here is update_missing_links at the bottom,
this is for after you have updated the db with the game status
... this will try to update games that have finiished status
yes but don't have youtube info"""

from typing import Dict
from typing import List
from typing import Tuple
import re
import sqlite3
from scripts.patterns import team_regex
from scripts.youtube_urls import pull_possible_video_urls
from app.db import engine, local_engine, Session, LocalSession
from sqlalchemy import text


def filter_for_highlights(video_info: list[dict]) -> list[dict]:
    "drop videos that don't have highlights in their title"
    if not video_info:
        return []
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


def to_chage_query():
    return (
        "SELECT full_date, home, away, id FROM schedule "
        "WHERE finished = 'yes' AND youtube_url = '';"
    )


def pull_finished_games(local=False):
    query = to_chage_query()
    session_maker = LocalSession if local else Session
    with session_maker() as session:
        to_change = session.execute(text(query)).mappings().all()
    return to_change


def format_games(
    games_info: List[Dict[str, str]]
) -> List[Tuple[re.Pattern, re.Pattern, re.Pattern, str]]:
    "assumes games info comes from a select full_date, home, away ,id query"
    regex = {
        team_name: re.compile(team_regex_pattern, re.IGNORECASE)
        for team_name, team_regex_pattern in team_regex().items()
    }
    return [
        (
            re.compile(
                format_date_for_displayed_comparison(game["full_date"])
            ),
            regex[game["home"]],
            regex[game["away"]],
            game["id"],
        )
        for game in games_info
    ]


def match_games_to_videos(
    video_info: List[Dict],
    games_info: List[Dict[str, str]],
) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    """
    this is naive with the double loop, various ways to make it better
    but everything is so small that it doesn't really matter
    still, better to sort by date desending in the query
    """
    formatted_games = format_games(games_info)
    url_id: List[Tuple[str, str, str]] = []
    missed_games = []
    for game in formatted_games:
        game_id = game[3]
        matching_items = game[:3]
        for video in video_info:
            missed = True
            if all(
                pattern.search(video["title"]) for pattern in matching_items
            ):
                url_id.append((video["url"], video["id"], game_id))
                missed = False
                break
        if missed:
            missed_games.append(game_id)
    return url_id, missed_games


def update_db_with_links(
    url_id_triples: List[Tuple[str, str, str]], local=False
) -> None:
    update = text(
        "UPDATE schedule "
        "SET youtube_url = :youtube_url, youtube_id = :youtube_id "
        "WHERE id = :id"
    )
    formatted_url_id_triples = [
        {"youtube_url": u, "youtube_id": y, "id": i}
        for u, y, i in url_id_triples
    ]

    session_maker = LocalSession if local else Session
    with session_maker() as session:
        session.execute(update, formatted_url_id_triples)
        session.commit()
    return


def update_missing_links(local=False):
    possible_videos = pull_possible_video_urls()
    highlight_videos = filter_for_highlights(possible_videos)
    games = pull_finished_games()
    url_id, missing_games = match_games_to_videos(highlight_videos, games)
    update_db_with_links(url_id, local)
    return missing_games
