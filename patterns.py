def team_regex():
    return {
        "arsenal": {"regex": r"arsenal", "name": "Arsenal"},
        "aston_villa": {"regex": r"villa", "name": "Aston Villa"},
        "bournemouth": {"regex": r"bournemouth", "name": "Bournemouth"},
        "brentford": {"regex": r"brentford", "name": "Brenford"},
        "brighton": {"regex": r"brighton", "name": "Brighton"},
        "burnley": {"regex": r"burnley", "name": "Burnley"},
        "chelsea": {"regex": r"chelsea", "name": "Chelsea"},
        "everton": {"regex": r"everton", "name": "Everton"},
        "forest": {"regex": r"forest", "name": "Nottingham Forest"},
        "fulham": {"regex": r"fulham", "name": "Fulham"},
        "leeds": {"regex": r"leeds", "name": "Leeds"},
        "liverpool": {"regex": "liverpool", "name": "Liverpool"},
        "man city": {
            "regex": r"(man c|manchester c)",
            "name": "Manchester City",
        },
        "man u": {
            "regex": r"(manchester u|man u)",
            "name": "Manchester United",
        },
        "newcastle": {"regex": "newcastle", "name": "Newcastle"},
        "palace": {"regex": r"palace", "name": "Crystal Palace"},
        "spurs": {"regex": r"spur", "name": "Tottenham Hotspur"},
        "sunderland": {"regex": r"sunderland", "name": "Sunderland"},
        "west ham": {"regex": r"west", "name": "West Ham"},
        "wolves": {"regex": "wolv", "name": "Wolves"},
    }


def mw_regex():
    return r"(matchweek|mw) ?\d\d?"


def day_num_regex():
    return (
        r"(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)( *\d\d?)?"
    )


def month_regex():
    return (
        r"(August|September|October|November|December|"
        r"January|February|March|April|May|June|July)"
    )


def time_regex():
    return r"\d\d?\:\d\d( *GMT)?"
