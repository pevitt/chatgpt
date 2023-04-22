from django.contrib import admin
from .models import AdviserMessages


# Register your models here.
@admin.register(AdviserMessages)
class AdviserMessagesAdmin(admin.ModelAdmin):
    list_display = ('profile',)
