from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from typing import Any
from application.api import ninja_api

urlpatterns: list[Any] = [
    path('admin/', admin.site.urls),
    path('api/', ninja_api.urls),
]

static_patterns = [
    re_path(r'^static/(?P<path>.*)$', serve),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='dev_robots.txt', content_type='text/plain'),
    ),
]

urlpatterns += static_patterns  # type: ignore