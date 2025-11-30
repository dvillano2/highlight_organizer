import sqlite3
import yt_dlp
from datetime import datetime
from app.db import engine, local_engine, Session, LocalSession
from sqlalchemy import text


def min_date_query():
    return """
        SELECT MIN(full_date)
        FROM schedule
        WHERE finished = 'yes' AND youtube_url = '';
        """


def get_min_finished_date_without_link(local=False):
    session_maker = LocalSession if local else Session

    with session_maker() as session:
        query = min_date_query()
        min_date = session.execute(text(query)).mappings().first()["min"]
    return min_date


def format_date_for_internal_comparison(date: str) -> str:
    no_time: str = date.split(" ")[0]
    return no_time.replace("-", "")


def get_youtube_chunk(start_index=1, chunck_size=50, channel_name="NBCSports"):
    url = f"https://www.youtube.com/@{channel_name}/videos"
    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "playlist_items": f"{start_index}-{start_index + chunck_size - 1}",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36"
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=False)
    return video_info["entries"]


def pull_single_upload_date(url: str):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        video_info = ydl.extract_info(url, download=False)
    return video_info["upload_date"]


def pull_videos_after_date(
    date: str, chunck_size: int = 50, channel_name: str = "NBCSports"
):
    full_info = []
    start_index = 1
    earliest_date_seen: str = date
    while date <= earliest_date_seen:
        video_info = get_youtube_chunk(
            start_index=start_index,
            chunck_size=chunck_size,
            channel_name=channel_name,
        )
        full_info.extend(video_info)
        last_url = video_info[-1]["url"]
        unformatted = pull_single_upload_date(last_url)
        earliest_date_seen = format_date_for_internal_comparison(unformatted)
        start_index += chunck_size
    return full_info


def pull_possible_video_urls(local=False):
    date = get_min_finished_date_without_link(local)
    if date is None:
        return
    return pull_videos_after_date(format_date_for_internal_comparison(date))
