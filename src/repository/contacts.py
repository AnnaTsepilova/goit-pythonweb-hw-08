from typing import List

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate, ContactStatusUpdate

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude={"tags"}, exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id)

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.dict(exclude={"tags"}, exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def update_status_contact(
        self, contact_id: int, body: ContactStatusUpdate
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            contact.done = body.done
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def search_contacts(self, search_field: str, query: str, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).where(Contact.__dict__[search_field].like(f"%{query}%")).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def birthdays_contacts(self, skip: int, limit: int) -> List[Contact]:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        stmt = select(Contact).where(Contact.birthday.between(today, next_week)).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()
