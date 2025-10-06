"""Urls to pull schedule info, multiples so the corroborate each other"""

from typing import Dict

URLS2526: Dict[str, str] = {
    "official": (
        "https://www.premierleague.com/en/news/4324539/"
        "all-380-fixtures-for-202526-premier-league-season"
    ),
}

URLS_BY_SEASON: Dict[str, Dict[str, str]] = {"2526": URLS2526}
