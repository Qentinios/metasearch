from django.urls import path

from website.views import HomeView, SearchView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search'),
    path('about', AboutView.as_view(), name='about'),
]
