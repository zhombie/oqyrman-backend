from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "image",
            "epub_cyrillic",
            "epub_latin",
            "description",
            "section_id",
            "section_name",
        ]
