from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.search_country_year, name='search_country_year'),
    path('countries/<str:country>/', views.countries_data, name='countries_data'),
    path('chart/', views.country_chart_view, name='country_chart'),
] 
 