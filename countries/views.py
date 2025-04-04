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

import os
from django.conf import settings
from django.shortcuts import render

# List of available country files (without `.txt`)
COUNTRY_CHOICES = [
    'australia', 'brazil', 'china', 'france', 'japan',
    'newZealand', 'northAmerica', 'southAfrica', 'uganda', 'uk',
    'yemen'
]

def parse_country_file(country):
    # Normalize to match file names
    filename = f"{country}.txt"
    file_path = os.path.join(settings.BASE_DIR, 'countries', 'countries_data', filename)

    years = []
    populations = []
    pollution = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                year = parts[0].split(':')[1].strip()
                pop = parts[1].split(':')[1].strip()
                poll = parts[2].split(':')[1].strip()

                years.append(year)
                populations.append(float(pop.replace(',', '')))
                pollution.append(float(poll.replace(',', '')))
    except FileNotFoundError:
        return None

    return {
        'country': country.title(),
        'years': years,
        'populations': populations,
        'pollution': pollution,
    }

def country_chart_view(request):
    chart_data = None
    selected_country = None

    if request.method == 'POST':
        selected_country = request.POST.get('country')
        if selected_country in COUNTRY_CHOICES:
            chart_data = parse_country_file(selected_country)

    return render(request, 'countries/chart.html', {
        'chart_data': chart_data,
        'countries': COUNTRY_CHOICES,
        'selected_country': selected_country
    })
