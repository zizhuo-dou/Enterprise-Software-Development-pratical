import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from .models import CountryData

COUNTRY_CHOICES = [
    'australia', 'brazil', 'china', 'france', 'japan',
    'newZealand', 'northAmerica', 'southAfrica', 'uganda', 'uk',
    'yemen'
]

def countries_data(request, country):
    data = CountryData.objects.filter(country=country).order_by('year')
    return render(request, 'countries/countries_data.html', {
        'data': data,
        'country': country
    })


from django.db.models import F

def search_country_year(request):
    from .models import CountryData

    country_years = CountryData.objects.values_list('country', 'year')
    country_year_map = {}

    for country, year in country_years:
        c = country.strip().title()
        if c not in country_year_map:
            country_year_map[c] = []
        if year not in country_year_map[c]:
            country_year_map[c].append(year)

    result = None
    error = None

    if request.method == 'POST':
        country = request.POST.get('country', '').strip().title()
        year = request.POST.get('year', '').strip()

        if not country or not year:
            error = "⚠️ Please enter both a country and a year."
        else:
            try:
                data = CountryData.objects.get(country=country, year=int(year))
                result = {
                    'country': data.country,
                    'year': data.year,
                    'population': data.population_mil,
                    'pollution_affected': data.pollution_affected_mil
                }
            except CountryData.DoesNotExist:
                error = "No data found for that country and year."
            except ValueError:
                error = "⚠️ Year must be a number."

    return render(request, 'countries/search_form.html', {
        'result': result,
        'error': error,
        'year_options': country_year_map,
        'selected_country': country,
        'selected_year': year
    })

def parse_country_file(country):
    filename = f"{country}.txt"
    file_path = os.path.join(settings.BASE_DIR, 'countries', 'countries_data', filename)

    years = []
    populations = []
    pollution = []

    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue  

                parts = line.split(',')
                if len(parts) < 3:
                    print(f"⚠️ Skipping line {line_number} (not enough commas): {line}")
                    continue

                try:
                    year_part = parts[0].split(':', 1)
                    pop_part = parts[1].split(':', 1)
                    poll_part = parts[2].split(':', 1)

                    if len(year_part) < 2 or len(pop_part) < 2 or len(poll_part) < 2:
                        print(f"⚠️ Skipping malformed line {line_number}: {line}")
                        continue

                    year = year_part[1].strip()
                    pop = pop_part[1].strip().replace(',', '')
                    poll = poll_part[1].strip().replace(',', '')

                    years.append(year)
                    populations.append(float(pop))
                    pollution.append(float(poll))

                except ValueError as e:
                    print(f"⚠️ Error parsing line {line_number}: {line} — {e}")
                    continue

    except FileNotFoundError:
        print(f"🚫 File not found: {file_path}")
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
        selected_country = request.POST.get('country', '').strip()
        if selected_country in COUNTRY_CHOICES:
            chart_data = parse_country_file(selected_country)

    return render(request, 'countries/chart.html', {
        'chart_data': chart_data,
        'countries': COUNTRY_CHOICES,
        'selected_country': selected_country
    })
