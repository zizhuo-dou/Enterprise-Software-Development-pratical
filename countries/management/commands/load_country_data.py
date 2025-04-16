import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from countries.models import CountryData

class Command(BaseCommand):
    """There was an issue with displaying the names as North America rather than north America. UK was also showing up as Uk. 
    All the below code is to make sure it displays correctly on the page. Maybe overkill but it was a lot of work just to get it to display
    correctly. """
    help = 'Load all country data files into the database'

    def handle(self, *args, **kwargs):
        print("Deleting all existing CountryData entries...")
        CountryData.objects.all().delete()

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = os.path.join(base_dir, 'countries/countries_data')

        display_names = {
            "uk": "UK",
            "northamerica": "North America",
            "southafrica": "South Africa",
            "southamerica": "South America",
            "newzealand": "New Zealand"
        }

        print("Deleting all existing CountryData entries...")
        CountryData.objects.all().delete()
        print("Database with incorrect names cleared.")

        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                name_raw = filename.replace('.txt', '').replace('_', '').replace('-', '').lower()
                country_name = display_names.get(name_raw, name_raw.title())  # Use clean name if mapped

                print(f"Loading data for {country_name} (raw: {name_raw})")

                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if not line:
                            continue

                        parts = line.split(',')
                        if len(parts) < 3:
                            print(f"Issues with line. Skipping bad line: {line}")
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
                            print(f"Year {year} added for {country_name}")
                        except (IndexError, ValueError) as e:
                            print(f"Issues with line. Skipping bad line: {line} — {e}")
