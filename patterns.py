def team_regex():
    return {
        "arsenal": r"arsenal",
        "aston_villa": r"villa",
        "bournemouth": r"bournemouth",
        "brentford": r"brentford",
        "brighton": r"brighton",
        "burnley": r"burnley",
        "chelsea": r"chelsea",
        "everton": r"everton",
        "forest": r"forest",
        "fulham": r"fulham",
        "leeds": r"leeds",
        "liverpool": "liverpool",
        "man city": r"(man c|manchester c)",
        "man u": r"(manchester u|man u)",
        "newcastle": "newcastle",
        "palace": r"palace",
        "spurs": r"spur",
        "sunderland": r"sunderland",
        "west ham": r"west",
        "wolves": r"wolv",
    }


def mw_regex():
    return r"(match|mw)"


def day_regex():
    return r"(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)"


def month_regex():
    return (
        r"(August|September|October|November|December|"
        r"January|February|March|April|May|June|July)"
    )


def month_num_regex():
    return r"\d\d?"

def time_regex():
    return r"\d\d?\:\d\d( *GMT)?"
