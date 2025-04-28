import uuid
from typing import List, Optional
from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

from litestar import Litestar, get, post, put, delete
from litestar.di import Provide
from litestar.exceptions import HTTPException

# ========== Настройки ==========

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# ========== SQLAlchemy ==========

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session_factory() as session:
        yield session

# ========== Модель User ==========

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# ========== Pydantic схемы ==========

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

class UserRead(BaseModel):
    id: str
    name: str
    surname: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # заменяет orm_mode в Pydantic v2

# ========== Эндпоинты ==========

@post("/users")
async def create_user(data: UserCreate, session: AsyncSession) -> UserRead:
    new_user = User(**data.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserRead.model_validate(new_user)

@get("/users")
async def list_users(session: AsyncSession) -> List[UserRead]:
    result = await session.execute(select(User))
    return [UserRead.model_validate(user) for user in result.scalars().all()]

@get("/users/{user_id:str}")
async def get_user(user_id: str, session: AsyncSession) -> UserRead:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@put("/users/{user_id:str}")
async def update_user(user_id: str, data: UserUpdate, session: AsyncSession) -> UserRead:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)

@delete("/users/{user_id:str}", status_code=204)
async def delete_user(user_id: str, session: AsyncSession) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()

# ========== Приложение ==========

async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = Litestar(
    route_handlers=[create_user, list_users, get_user, update_user, delete_user],
    on_startup=[on_startup],
    dependencies={"session": Provide(get_session)},  # Указываем зависимость для session только здесь
)
