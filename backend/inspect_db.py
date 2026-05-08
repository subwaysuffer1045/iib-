import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5432/iib_india")
    
    r = await conn.fetch("SELECT typname, typtype FROM pg_type WHERE typtype = 'e' ORDER BY typname")
    print("All ENUM types in DB:")
    for row in r:
        print(f"  - {row['typname']}")
    
    r2 = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
    print("\nAll tables in DB:")
    for row in r2:
        print(f"  - {row['tablename']}")
    
    await conn.close()

asyncio.run(check())
