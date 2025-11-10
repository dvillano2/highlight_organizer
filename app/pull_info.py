import sqlite3


def pull_db_info():
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT mw, day, num, month, home, away, youtube_url FROM schedule ORDER BY full_date"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
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
        if row[0] not in final_dict:
            final_dict[row[0]] = {}
        date_str = f"{row[1]} {row[3]} {row[2]}"
        if date_str not in final_dict[row[0]]:
            final_dict[row[0]][date_str] = {}
        final_dict[row[0]][date_str][f"{row[4]} v {row[5]}"] = row[6]
    drop_empty_weeks(final_dict)
    return final_dict
