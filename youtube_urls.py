import sqlite3
import yt_dlp
from datetime import datetime


def get_min_finished_date_without_link():
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MIN(full_date) FROM SCHEDULE WHERE "
        "finished = 'yes AND 'youtube_url='';"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]


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
        earliest_date_seen = pull_single_upload_date(last_url)
        start_index += chunck_size
    return full_info


def pull_possible_video_urls():
    date = get_min_finished_date_without_link()
    if date is None:
        return
    return pull_videos_after_date(date)
