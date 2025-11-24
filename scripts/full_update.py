"""run this to find played games and update links"""

from update_season_data import update_schedule
from match_video_to_database import update_missing_links

if __name__ == "__main__":
    update_schedule()
    update_missing_links()
