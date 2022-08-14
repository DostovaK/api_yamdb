from django.contrib import admin

from .models import User


@admin.register(User)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'role',
        'first_name',
        'last_name',
        'email',
        'bio',
        'confirmation_code'
    )
    search_fields = ('username', )
    list_filter = ('username', )
