import sqlite3
from pull_season_data import organize_mws, mws_to_df


def get_min_unfinished_mw():
    conn = sqlite3.connect("PL_20252026_season.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(mw) FROM schedule WHERE finished='no';")
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    return int(rows[0])


def update_query():
    return """
    UPDATE schedule
    SET
        day = tmp.day,
        num = tmp.num,
        month = tmp.month,
        time = tmp.time,
        year = tmp.year,
        timezone = tmp.timezone,
        full_date = tmp.full_date,
        finished = tmp.finished
    FROM tmp
    WHERE schedule.id = tmp.id
    AND (schedule.finished = 'no' OR schedule.youtube_url = '');
    """


def update_schedule():
    min_unplayed_mw = get_min_unfinished_mw()
    new_schedule = organize_mws(min_unplayed_mw)
    df_new_schedule = mws_to_df(new_schedule)

    query = update_query()

    conn = sqlite3.connect("PL_20252026_season.db")
    df_new_schedule.to_sql("tmp", conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.execute("DROP TABLE tmp;")
    conn.commit()
    cursor.close()
    conn.close()
    return


if __name__ == "__main__":
    update_schedule()
