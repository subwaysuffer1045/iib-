import asyncio
import asyncpg
from urllib.parse import urlparse

async def check_db():
    url = "postgresql://postgres:postgres@localhost:5432/iib_india"
    try:
        conn = await asyncpg.connect(url)
        print("Successfully connected to the database!")
        await conn.close()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")

if __name__ == "__main__":
    asyncio.run(check_db())
