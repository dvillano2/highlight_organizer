import sqlite3
from pull_season_data import pull_single_mw, mws_to_df


def update_mw(mw=int):
    mw_games = pull_single_mw(mw)
    finished_games = {
        key: value
        for key, value in mw_games.items()
        if value["finished"] == "yes"
    }
    mw_df = mws_to_df(finished_games)

    conn = sqlite3.connect("PL_20252026_season.db")
    mw_df.to_sql("temp", conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule SET day, num, month, time, year, timezone, "
        "full_date, finished FROM temp WHERE schedule.id = temp.id;"
    )
    cursor.execute("DROP TABLE temp;")
    conn.commit()
    cursor.close()
    conn.close()
    return
