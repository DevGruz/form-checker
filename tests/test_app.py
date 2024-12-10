from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app, mongo_settings


@pytest.fixture(scope="session")
async def init_db() -> AsyncGenerator[None, None]:
    await mongo_settings.init_db("data/templates.json")
    yield
    await mongo_settings.drop_database()
    mongo_settings.get_client().close()


@pytest.fixture
async def client(init_db: None) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.mark.asyncio
async def test_get_form_success(client: AsyncClient):
    data = {"applicant_name": "text", "applicant_email": "text@email.com"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("/get_form", data=data, headers=headers)

    assert response.status_code == 200
    assert response.json() == "Job Application Form"


@pytest.mark.asyncio
async def test_get_form_empty_body(client: AsyncClient):
    data = {}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("/get_form", data=data, headers=headers)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Request body is required and cannot be empty. Provide valid data in the request."
    }


@pytest.mark.asyncio
async def test_get_form_dynamic_fields(client: AsyncClient):
    data = {"f_name1": "value1", "f_name2": "text@email.com"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = await client.post("/get_form", data=data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"f_name1": "text", "f_name2": "email"}
