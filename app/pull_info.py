from .db import SessionLocal
from sqlalchemy import text


def pull_db_info():
    session = SessionLocal()
    rows = (
        session.execute(
            text(
                "SELECT mw, day, num, month, home, away, youtube_id FROM schedule ORDER BY full_date"
            )
        )
        .mappings()
        .all()
    )
    session.close()
    return rows


def drop_empty_weeks(structured_dict):
    mw_flags = {mw: 0 for mw in structured_dict.keys()}

    for mw, dates in structured_dict.items():
        for games in dates.values():
            for link in games.values():
                if link != "":
                    mw_flags[mw] += 1

    for mw, flag in mw_flags.items():
        if flag == 0:
            del structured_dict[mw]


def make_dict(rows):
    final_dict = {}
    for row in rows:
        if row["mw"] not in final_dict:
            final_dict[row["mw"]] = {}
        date_str = f"{row['day']} {row['month']} {row['num']}"
        if date_str not in final_dict[row["mw"]]:
            final_dict[row["mw"]][date_str] = {}
        final_dict[row["mw"]][date_str][f"{row['home']} v {row['away']}"] = (
            row["youtube_id"]
        )
    drop_empty_weeks(final_dict)
    return final_dict
