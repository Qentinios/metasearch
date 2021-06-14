from django.urls import path

from website.views import HomeView, SearchView, AboutView, register_request, login_request, logout_request,\
    OfferDetailsView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    path('about', AboutView.as_view(), name='about'),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path("offer/<int:pk>", OfferDetailsView.as_view(), name="offer-details"),
]
