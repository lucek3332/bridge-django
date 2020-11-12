from django.contrib import admin
from .models import Board


class BoardAdmin(admin.ModelAdmin):
    list_display = ("unique_id", "table", "contract", "score", "created")
    list_filter = ("table", "contract", "created")
    search_fields = ("contract", "score")


admin.site.register(Board, BoardAdmin)
