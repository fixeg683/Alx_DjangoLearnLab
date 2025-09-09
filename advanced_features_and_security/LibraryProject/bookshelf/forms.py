# bookshelf/forms.py
from django import forms
from .models import Book, CustomUser


class ExampleForm(forms.Form):
    """A simple example form (for testing CSRF tokens, etc.)."""

    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}),
        required=True,
        label="Message",
    )


class BookForm(forms.ModelForm):
    """ModelForm for the Book model."""

    class Meta:
        model = Book
        fields = ["title", "author"]


class CustomUserCreationForm(forms.ModelForm):
    """Form for creating new users (extends CustomUser)."""

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput, strip=False
    )
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput, strip=False
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don’t match ❗")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
