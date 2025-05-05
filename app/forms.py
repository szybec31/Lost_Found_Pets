from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserModel

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserModel
        #fields = ("email", "phone")
        fields = ('email', 'first_name', 'last_name', 'phone', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        #fields = ("email", "phone")
        fields = ('email', 'first_name', 'last_name', 'phone', 'password')