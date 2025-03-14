from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.utils.translation import gettext_lazy as _


class ProjectAdminSite(admin.AdminSite):
    site_header = _('Управление <project_name>')
    site_title = _('Управление <project_name>')
    index_title = _('')


class ProjectAdminConfig(AdminConfig):
    default_site = "application.admin.ProjectAdminSite"
