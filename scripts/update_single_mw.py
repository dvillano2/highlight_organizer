from pull_season_data import pull_single_mw, mws_to_df
from update_season_data import update_query
from sqlalchemy import text
from app.db import engine, Session, local_engine, LocalSession
from sqlalchemy.exc import SQLAlchemyError


def update_mw(mw: int, local: bool = False):
    mw_games = pull_single_mw(mw)
    finished_games = {
        key: value
        for key, value in mw_games.items()
        if value["finished"] == "yes"
    }
    if not finished_games:
        return
    mw_df = mws_to_df(finished_games)

    current_engine = local_engine if local else engine
    session_maker = LocalSession if local else Session

    mw_df.to_sql("tmp", con=current_engine, if_exists="replace", index=False)

    query = update_query()
    with session_maker() as session:
        try:
            session.execute(text(query))
            session.execute(text("DROP TABLE tmp;"))
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
    return
