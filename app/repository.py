from pymongo.asynchronous.collection import AsyncCollection


class FormRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def find_one_or_none(self, query: dict) -> dict | None:
        result = await self.collection.find_one(query)
        return result
