from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].help_text = 'Wymagane. 150 znaków lub mniej. Litery, liczby i @/./+/-/_ .'
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].help_text = '<ul> <li> Twoje hasło nie może być zbyt podobne do Twoich innych danych osobowych. </li> <li> Twoje hasło musi zawierać co najmniej 8 znaków. </li> <li> Twoje hasło nie może być powszechnie używane. </li> <li> Twoje hasło nie może składać się wyłącznie z cyfr. </li> </ul>'
        self.fields['password2'].label = 'Powtórz hasło'
        self.fields['password2'].help_text = 'Podaj to samo hasło dla weryfikacji.'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['password'].label = 'Hasło'
