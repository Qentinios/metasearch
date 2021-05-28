from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from website.forms import NewUserForm, LoginUserForm


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class SearchView(TemplateView):
    template_name = 'search.html'


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja zakończona sukcesem.")
            return redirect("index")
        messages.error(request, "Rejestracja nie powiodła się. Złe dane.")
    form = NewUserForm
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Zalogowano jako {username}.")
                return redirect("index")
            else:
                messages.error(request, "Zły login lub hasło.")
        else:
            messages.error(request, "Zły login lub hasło.")
    form = LoginUserForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano.")
    return redirect("index")
