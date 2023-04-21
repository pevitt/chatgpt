from django.contrib import admin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname',)

    def email(self, obj):
        return obj.user.email

    def firstname(self, obj):
        return obj.user.first_name
