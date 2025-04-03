from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserModel

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ("email", "phone_number")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ("email", "phone_number")