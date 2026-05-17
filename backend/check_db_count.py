import asyncio
from app.database import engine
from sqlalchemy import text

async def main():
    async with engine.connect() as c:
        r = await c.execute(text("SELECT count(*) FROM internships"))
        print("Internships count:", r.scalar())
        
        r2 = await c.execute(text("SELECT count(*) FROM companies"))
        print("Companies count:", r2.scalar())
        
        # Let's print the internships titles if any
        r3 = await c.execute(text("SELECT title, stipend_min, apply_link FROM internships LIMIT 5"))
        print("Sample Internships:")
        for row in r3:
            print(f"  - {row[0]} | Stipend: {row[1]} | Link: {row[2]}")

asyncio.run(main())
