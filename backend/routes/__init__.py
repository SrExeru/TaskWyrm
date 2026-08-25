from routes.auth import auth_router
from routes.user import user_router

all_routes = [
    auth_router,
    user_router
]