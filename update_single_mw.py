import sqlite3
from pull_season_data import pull_single_mw, mws_to_df
from update_season_data import update_query


def update_mw(mw=int):
    mw_games = pull_single_mw(mw)
    finished_games = {
        key: value
        for key, value in mw_games.items()
        if value["finished"] == "yes"
    }
    if not finished_games:
        return
    mw_df = mws_to_df(finished_games)

    conn = sqlite3.connect("PL_20252026_season.db")
    mw_df.to_sql("tmp", conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor = conn.cursor()
    query = update_query()
    cursor.execute(query)
    cursor.execute("DROP TABLE temp;")
    conn.commit()
    cursor.close()
    conn.close()
    return
