from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin[User]):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    search_fields = ('username',)
    exclude = ('password',)

admin.site.register(User, UserAdmin)