from django.utils.translation import gettext_lazy as _
from ninja import NinjaAPI
from users.api import user_router

ninja_api = NinjaAPI(
    title=_("project API"),
    auth=None,
    csrf=True,
    description=_("API for project"),
    urls_namespace="api",
)


ninja_api.add_router('/users/', user_router, tags=["Users"])