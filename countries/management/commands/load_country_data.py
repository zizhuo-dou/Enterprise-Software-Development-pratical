import os
from pathlib import Path
from django.core.management.base import BaseCommand
from countries.models import CountryData

class Command(BaseCommand):
    help = 'Load all country data files into the database'

    def handle(self, *args, **kwargs):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = os.path.join(base_dir, 'countries/countries_data')

        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                country_name = filename.replace('.txt', '').capitalize()
                CountryData.objects.filter(country=country_name).delete()
                print(f"Loading data for {country_name}...")

                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if not line:
                            continue  # skip empty lines

                        parts = line.split(',')
                        if len(parts) < 3:
                            print(f"⚠️ Skipping malformed line: {line}")
                            continue

                        try:
                            year = int(parts[0].split(':')[1].strip())
                            population = float(parts[1].split(':')[1].strip().replace(',', ''))
                            pollution = float(parts[2].split(':')[1].strip().replace(',', ''))

                            CountryData.objects.create(
                                year=year,
                                country=country_name,
                                population_mil=population,
                                pollution_affected_mil=pollution
                            )
                            print(f"  ✔ Year {year} added for {country_name}")
                        except (IndexError, ValueError) as e:
                            print(f"⚠️ Skipping bad line in {country_name}: {line.strip()} — {e}")
                            continue