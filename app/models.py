from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[Optional[datetime.now]]
    updated_at: Mapped[Optional[datetime.now]]