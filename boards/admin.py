from django.contrib import admin
from .models import Board, Hand


class BoardAdmin(admin.ModelAdmin):
    list_display = ("unique_id", "table", "player", "final_result", "score", "created")
    list_filter = ("table", "player", "contract", "created")
    search_fields = ("contract", "score")


admin.site.register(Board, BoardAdmin)
admin.site.register(Hand)
