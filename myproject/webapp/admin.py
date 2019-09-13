from django.contrib import admin
from .models import Book


class BookModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title"]

    class Meta:
        model = Book


admin.site.register(Book, BookModelAdmin)