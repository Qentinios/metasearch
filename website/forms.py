from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from website.models import Offer


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


class SearchForm(ModelForm):
    price_min = forms.IntegerField(min_value=0, required=False)
    price_max = forms.IntegerField(min_value=0, required=False)
    area_min = forms.IntegerField(min_value=0, required=False)
    area_max = forms.IntegerField(min_value=0, required=False)

    class Meta:
        model = Offer
        fields = ('type', 'website', 'area_min', 'area_max', 'rooms', 'price_min', 'price_max', 'city')

    def __init__(self, get=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-element row'
        self.helper.wrapper_class = 'col-md-2'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'control-form'

        self.fields['rooms'].required = False
        self.fields['city'].required = False
        self.fields['website'].required = False

        city = get.get('city', None)
        if get.get('city', None):
            self.fields['city'].initial = city

        type = get.get('type', None)
        if get.get('type', None):
            self.fields['type'].initial = type
        else:
            self.fields['type'].initial = Offer.TYPES.flat

        website = get.get('site', None)
        if get.get('site', None):
            self.fields['website'].initial = website
