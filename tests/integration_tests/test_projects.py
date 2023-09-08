import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.datasource.database import db_connection


@db_connection()
async def _insert_project(
    name: str,
    description: str,
    async_session: AsyncSession,
) -> None:
    await async_session.execute(
        statement=text(
            """
            INSERT INTO project
                (name, description)
            VALUES
                (:name, :description)
        """
        ),
        params={
            "name": name,
            "description": description,
        },
    )


@pytest.mark.asyncio
async def test_project(client: AsyncClient, session: AsyncSession) -> None:
    for project in [
        {"name": "name01", "description": "description01"},
        {"name": "name02", "description": "description02"},
    ]:
        await _insert_project(project["name"], project["description"])

    # get list
    response = await client.get("/projects")
    assert response.status_code == 200, response.json()
    response_projects = response.json().get("projects")
    assert len(response_projects) == 2
    assert response_projects[0].get("id") == 1
    assert response_projects[0].get("name") == "name01"
    assert response_projects[0].get("description") == "description01"
    assert response_projects[1].get("id") == 2
    assert response_projects[1].get("name") == "name02"
    assert response_projects[1].get("description") == "description02"
