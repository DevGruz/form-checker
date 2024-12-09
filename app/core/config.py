from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoConfig(BaseSettings):
    HOST: str = Field(validation_alias="MONGO_HOST")
    PORT: int = Field(validation_alias="MONGO_PORT")
    DB_NAME: str = Field(validation_alias="MONGO_DATABASE_NAME")
    COLLECTION: str = Field(validation_alias="MONGO_COLLECTION")
    ROOT_USERNAME: str = Field(validation_alias="MONGO_ROOT_USERNAME")
    ROOT_PASSWORD: str = Field(validation_alias="MONGO_ROOT_PASSWORD")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def URL(self):
        auth_part = (
            f"{self.ROOT_USERNAME}:{self.ROOT_PASSWORD}@"
            if self.ROOT_USERNAME and self.ROOT_PASSWORD
            else ""
        )
        return f"mongodb://{auth_part}{self.HOST}:{self.PORT}"


class Config(BaseSettings):
    PROJECT_NAME: str
    INIT_DATA_IN_DATABASE: bool

    MONGO: MongoConfig = MongoConfig()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
