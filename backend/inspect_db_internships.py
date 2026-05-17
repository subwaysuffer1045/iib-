import asyncio
from app.database import AsyncSessionLocal
from app.models.internship import Internship
from app.models.company import Company
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Internship))
        internships = res.scalars().all()
        print(f"Total internships in DB: {len(internships)}")
        for i, intern in enumerate(internships):
            comp_res = await db.execute(select(Company).where(Company.id == intern.company_id))
            comp = comp_res.scalar_one_or_none()
            comp_name = comp.name if comp else "Unknown"
            stipend_text = (intern.stipend_text or "").replace("\u20b9", "Rs.")
            print(f"{i+1}. [{intern.status.value}] {intern.title} at {comp_name} ({intern.work_mode.value}) - {stipend_text} - {intern.apply_link}")

if __name__ == "__main__":
    asyncio.run(main())
