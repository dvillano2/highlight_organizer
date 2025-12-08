"""run this to find played games and update links"""

from scripts.update_season_data import update_schedule
from scripts.match_video_to_database import update_missing_links
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

if __name__ == "__main__":
    update_schedule()
    update_missing_links()
