from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, DetailView

from scrappers.tasks import Search
from website.forms import NewUserForm, LoginUserForm, SearchForm
from website.models import Offer


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['get'] = self.request.GET
        return form_kwargs

    def form_valid(self, form):
        search = Search(form.cleaned_data)
        offers = search.search()

        context_data = self.get_context_data(form=form)
        context_data['offers'] = offers
        return self.render_to_response(context_data)


class OfferDetailsView(DetailView):
    template_name = 'offer.html'
    model = Offer
    queryset = Offer.objects.all()


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
