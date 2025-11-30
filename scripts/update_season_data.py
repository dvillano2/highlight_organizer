from sqlalchemy import text
from pull_season_data import organize_mws, mws_to_df
from app.db import engine, Session, local_engine, LocalSession
from sqlalchemy.exc import SQLAlchemyError


def get_min_unfinished_mw(local=False):
    session_maker = LocalSession if local else Session
    with session_maker() as session:
        query = "SELECT MIN(mw) FROM schedule WHERE finished='no';"
        mw = session.execute(text(query)).mappings().first()["min"]
    return mw


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


def update_schedule(local=False):
    min_unplayed_mw = get_min_unfinished_mw()
    new_schedule = organize_mws(min_unplayed_mw)
    df_new_schedule = mws_to_df(new_schedule)

    query = update_query()
    current_engine = local_engine if local else engine
    session_maker = LocalSession if local else Session
    session = session_maker()

    df_new_schedule.to_sql(
        "tmp", con=current_engine, if_exists="replace", index=False
    )
    with session_maker() as session:
        try:
            session.execute(text(query))
            session.execute(text("DROP TABLE tmp;"))
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
    return


if __name__ == "__main__":
    update_schedule()
