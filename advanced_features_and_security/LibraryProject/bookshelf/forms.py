# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "description"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title


class SecureSearchForm(forms.Form):
    q = forms.CharField(label="Search", required=False, max_length=100)

    def cleaned_term(self) -> str:
        # helper to avoid repetition
        return self.cleaned_data.get("q", "").strip()
