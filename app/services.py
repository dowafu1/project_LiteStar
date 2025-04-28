from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from app.models import User

class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User
