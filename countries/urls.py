from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_country_year, name='home'),  # Homepage shows search form
    path('countries/<str:country>/', views.countries_data, name='countries_data'),
    path('search/', views.search_country_year, name='search_country_year'),
    path('chart/', views.country_chart_view, name='country_chart'),
]
