"""run this to find played games and update links"""

from update_season_date import update_schedule
from match_videos_to_db import update_missing_links

if __name__ == "__main__":
    update_schedule()
    update_missing_links()
