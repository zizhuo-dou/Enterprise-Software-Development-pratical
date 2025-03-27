from django.urls import path
from . import views

urlpatterns = [
    path('', views.countries_data, name='countries_list'),
    path('countries/<str:country>', views.countries_data, name='countries_data'),
    path('search/', views.search_country_year, name='search_country_year'),
]
