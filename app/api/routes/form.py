from fastapi import APIRouter, Depends, Request
from app.api.deps import get_form_service, FormService

router = APIRouter()


@router.post("/get_form")
async def get_form(request: Request, service: FormService = Depends(get_form_service)):
    form_data = await request.form()
    result = await service.search_template_forms_by_fields(form_data)
    return result
