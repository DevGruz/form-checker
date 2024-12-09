from fastapi import APIRouter

from app.api.routes import form

api_router = APIRouter()

api_router.include_router(form.router, tags=["forms"])
