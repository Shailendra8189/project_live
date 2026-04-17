from django import forms
from .models import Lead, Category

# from agent.models import Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "age",
            "agent",
            "description",
            "phone_number",
            "email",
        )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(LeadModelForm, self).__init__(*args, **kwargs)
        if request.user.role == "agent":
            self.fields.pop("agent")


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("type",)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {
            "username": UsernameField,
        }


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("category",)
