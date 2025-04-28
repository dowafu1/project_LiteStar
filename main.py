from litestar import Litestar
from app.db import alchemy_plugin
from app.routes import UserController

app = Litestar(
    route_handlers=[UserController],
    plugins=[alchemy_plugin],
)
