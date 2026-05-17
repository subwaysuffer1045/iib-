import asyncio
from app.database import AsyncSessionLocal
from app.models.internship import Internship
from app.models.company import Company
from sqlalchemy import delete

async def main():
    async with AsyncSessionLocal() as db:
        print("Deleting all internships...")
        await db.execute(delete(Internship))
        print("Deleting all companies...")
        await db.execute(delete(Company))
        await db.commit()
        print("Database reset completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
