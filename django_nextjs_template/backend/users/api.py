from ninja import Router
from django.http import HttpRequest
from dataorm.api import single_item
from dataorm.auth import async_get_user
from users.schema import UserData

current_user_router = Router()

@single_item(current_user_router, url='/', response_type=UserData)
async def get_current_user(request: HttpRequest):
    user = await async_get_user(request)
    return UserData(id=user.id, username=user.username, is_superuser=user.is_superuser) # type: ignore