from ninja import Router, Path
from django.http import HttpRequest
from django_utils.api import single_item
from django_utils.auth import async_get_user
from users.models import User
from users.schema import UserData, CurrentUserData, CurrentUserResponse

user_router = Router()

@single_item(user_router, url='current_user/', response_type=CurrentUserResponse)
async def get_current_user(request: HttpRequest):
    user = await async_get_user(request)
    return CurrentUserResponse(
        user=CurrentUserData(id=user.id, username=user.username, is_superuser=user.is_superuser)
    )


@single_item(user_router, url='by_id/{user_id}', response_type=UserData)
async def get_user_by_id(request: HttpRequest, user_id: Path[int]):
    user = await User.objects.aget(id=user_id)
    return UserData(id=user.id, username=user.username)


@single_item(user_router, url='by_username/{username}', response_type=UserData)
async def get_user_by_username(request: HttpRequest, username: Path[str]):
    user = await User.objects.aget(username=username)
    return UserData(id=user.id, username=user.username)