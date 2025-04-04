from .models import CountryData

def countries_data(request, country):
    data = CountryData.objects.filter(country=country).order_by('year')
    return render(request, 'countries/countries_data.html', {'data': data, 'country': country})


from django.shortcuts import render
from .models import CountryData

def search_country_year(request):
    result = None
    if request.method == 'POST':
        country = request.POST.get('country').capitalize()
        year = request.POST.get('year')

        try:
            data = CountryData.objects.get(country=country, year=year)
            result = {
                'country': data.country,
                'year': data.year,
                'population': data.population_mil,
                'pollution_affected': data.pollution_affected_mil
            }
        except CountryData.DoesNotExist:
            result = "No data found for that country and year."

    return render(request, 'countries/search_form.html', {'result': result})
