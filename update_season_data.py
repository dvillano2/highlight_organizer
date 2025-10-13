import sqlite3
from pulling_season_data import organize_mws, mws_to_df


def get_min_unfinished_mw():
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(mw) FROM schedule WHERE finished='no';")
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    return int(rows[0])


def update_schedule():
    min_unplayed_mw = get_min_unfinished_mw()
    new_schedule = organize_mws(min_unplayed_mw)
    df_new_schedule = mws_to_df(new_schedule)

    conn = sqlite3.connect("PL_20252026_season.db")
    df_new_schedule.to_sql("temp", conn, if_exists="replace", index=False)
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


if __name__ == "__main__":
    update_schedule()
