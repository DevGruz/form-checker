from fastapi import HTTPException, status

from app.repository import FormRepository
from app.validators import FormFieldValidator


class FormService:
    def __init__(self, repository: FormRepository, validator: FormFieldValidator):
        self._repository = repository
        self._validator = validator

    async def search_template_forms_by_fields(self, form_data: dict) -> dict:
        if not form_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request body is required and cannot be empty. Provide valid data in the request.",
            )
        fields_with_types = {
            key: self._validator.validate(value) for key, value in form_data.items()
        }

        matching_template = await self._repository.find_one_or_none(
            query=fields_with_types
        )

        if matching_template:
            return matching_template.get("name")

        return fields_with_types
