import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('db/database.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, description TEXT)")
    db.commit()


async def create_profile():
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(
        key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?)", (user_id, ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile WHERE user_id == '{}' SET description = '{}'".format(
            user_id), data['description'])
        db.commit()
