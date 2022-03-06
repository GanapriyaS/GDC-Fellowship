from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.forms import ModelForm, ValidationError
from tasks.models import Task, Report

# Customising signup form
class UserSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Repeat password",
            }
        )


# Form to get task details
class TaskCreateForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise ValidationError("Data too small")
        return title.upper()

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "completed"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget.attrs.update(
            {
                "rows": "1",
                "placeholder": "Description",
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["title"].widget.attrs.update(
            {
                "placeholder": "Title",
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["priority"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["status"].widget.attrs.update(
            {
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
            }
        )
        self.fields["completed"].widget.attrs.update(
            {
                "class": "ml-2 mb-4 focus:outline-none",
            }
        )


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded-r-full focus:outline-none",
                "placeholder": "Password",
            }
        )
    )


# Form to set remainder time
class EmailReportForm(ModelForm):
    class Meta:
        model = Report
        widgets = {
            "remainder_time": forms.TimeInput(
                attrs={
                    "class": "w-full pl-4 pr-6 py-4 font-bold placeholder-gray-900 rounded mb-4 focus:outline-none",
                    "placeholder": "HH:MM",
                }
            )
        }
        fields = ["remainder_time", "disabled"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["disabled"].widget.attrs.update(
            {
                "class": "ml-2 mb-4 focus:outline-none",
            }
        )
