from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession  # Импортируем AsyncSession для аннотации типов
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services import UserRepository

# Обновляем функцию предоставления репозитория с аннотацией типа для db_session
async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)

class UserController(Controller):
    path = "/users"
    dependencies = {"repo": Provide(provide_user_repo)}

    @get("/", return_dto=list[UserRead])
    async def list_users(self, repo: UserRepository) -> list[UserRead]:
        return await repo.list()

    @get("/{user_id:uuid}", return_dto=UserRead)
    async def get_user(self, user_id: UUID, repo: UserRepository) -> UserRead:
        return await repo.get(user_id)

    @post("/", return_dto=UserRead)
    async def create_user(self, data: UserCreate, repo: UserRepository) -> UserRead:
        return await repo.add(data)

    @put("/{user_id:uuid}", return_dto=UserRead)
    async def update_user(self, user_id: UUID, data: UserUpdate, repo: UserRepository) -> UserRead:
        return await repo.update(user_id, data)

    @delete("/{user_id:uuid}")
    async def delete_user(self, user_id: UUID, repo: UserRepository) -> None:
        await repo.delete(user_id)

user_router = UserController
