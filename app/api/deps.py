from fastapi import Depends
from app.services import FormService
from app.repository import FormRepository
from app.validators import FormFieldValidator
from app.core.db import mongo_settings


async def get_form_collection():
    yield mongo_settings.get_collection()


async def get_form_repository(collection=Depends(get_form_collection)):
    yield FormRepository(collection)


async def get_form_validator():
    yield FormFieldValidator()


async def get_form_service(
    repository: FormRepository = Depends(get_form_repository),
    validator: FormFieldValidator = Depends(get_form_validator),
):
    yield FormService(repository, validator)
