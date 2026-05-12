import aiosqlite
import asyncio
import os

class Database:
    def __init__(self, db_path="data/database.db"):
        os.makedirs("data", exist_ok=True)
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS vip (
                user_id INTEGER PRIMARY KEY
            )''')
            await db.execute('''CREATE TABLE IF NOT EXISTS economy (
                user_id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 100
            )''')
            await db.commit()

    async def is_vip(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT 1 FROM vip WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone() is not None

db = Database()
