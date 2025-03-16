from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactModel, ContactUpdate, ContactStatusUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel):
        return await self.contact_repository.create_contact(body)

    async def get_contacts(self, skip: int, limit: int):
        return await self.contact_repository.get_contacts(skip, limit)

    async def get_contact(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        return await self.contact_repository.update_contact(contact_id, body)

    async def update_status_contact(self, contact_id: int, body: ContactStatusUpdate):
        return await self.contact_repository.update_status_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.contact_repository.remove_contact(contact_id)

    async def search_contacts(self, search_field: str, query: str, skip: int, limit: int):
        return await self.contact_repository.search_contacts(search_field, query, skip, limit)

    async def birthdays_contacts(self, skip: int, limit: int):
        return await self.contact_repository.birthdays_contacts(skip, limit)
