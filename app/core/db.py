from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
import json

from app.core.config import config


class AsyncMongoSettings:
    def __init__(self, client: AsyncMongoClient, db_name: str, collection: str):
        self._client = client
        self._db_name = db_name
        self._collection_name = collection
        self._db = self._client[self._db_name]
        self._collection = self._db[self._collection_name]

    def get_client(self) -> AsyncMongoClient:
        return self._client

    def get_db(self) -> AsyncDatabase:
        return self._db

    def get_collection(self) -> AsyncCollection:
        return self._collection

    def client_close(self) -> None:
        self._client.close()

    async def drop_database(self):
        await self._client.drop_database(self._db_name)

    async def init_db(self, filename: str) -> str:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                templates = json.load(file)
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден.")
            templates = []

        collection_exists = (
            self._collection_name in await self._db.list_collection_names()
        )

        if not collection_exists:
            if templates:
                await self._collection.insert_many(templates)
                print(
                    f"Добавлено {len(templates)} шаблонов в коллекцию '{self._collection}'."
                )
            else:
                print("Нет данных для инициализации.")
        else:
            print(f"Коллекция '{self._collection}' уже существует.")


client = AsyncMongoClient(
    host=config.MONGO.URL,
    port=config.MONGO.PORT,
    username=config.MONGO.ROOT_USERNAME,
    password=config.MONGO.ROOT_PASSWORD,
)

mongo_settings = AsyncMongoSettings(
    client=client,
    db_name=config.MONGO.DB_NAME,
    collection=config.MONGO.COLLECTION,
)
