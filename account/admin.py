from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPhoto, Subscriber, Like, Dislike
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets, (
            'User role',
            {
                'fields': (
                    'gender',
                    'city',
                    'avatar'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserPhoto)
admin.site.register(Subscriber)
admin.site.register(Like)
admin.site.register(Dislike)
