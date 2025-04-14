from django.test import TestCase, Client
from django.urls import reverse
from django.apps import apps
from countries.apps import CountriesConfig
from countries.models import CountryData
from countries.views import parse_country_file
from django.conf import settings

import os


# ✅ App Configuration Tests
class AppConfigTests(TestCase):
    def test_app_config_name(self):
        self.assertEqual(CountriesConfig.name, 'countries')

    def test_app_is_registered(self):
        app_config = apps.get_app_config('countries')
        self.assertIsInstance(app_config, CountriesConfig)


# 🌐 View Tests
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.country = 'australia'
        self.year = 1990
        CountryData.objects.create(
            country=self.country,
            year=self.year,
            population_mil=17.3,
            pollution_affected_mil=5.52
        )

    def test_search_country_year_view_get(self):
        response = self.client.get(reverse('search_country_year'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countries/search_form.html')

    def test_search_country_year_view_post_valid(self):
        response = self.client.post(reverse('search_country_year'), {
            'country': self.country,
            'year': self.year
        })
        self.assertContains(response, 'australia')  # match your template’s capitalization

    def test_countries_data_view(self):
        response = self.client.get(reverse('countries_data', args=[self.country]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countries/countries_data.html')


# 🧬 Model Tests
class CountryDataModelTests(TestCase):
    def test_model_creation(self):
        entry = CountryData.objects.create(
            country='australia',
            year=1990,
            population_mil=17.3,
            pollution_affected_mil=5.52
        )
        self.assertEqual(entry.country, 'australia')
        self.assertEqual(entry.year, 1990)


# 🧾 Utility Function Tests
class ParseCountryFileTests(TestCase):
    def test_parse_valid_file(self):
        # Uses the real file from your dataset: australia.txt
        parsed = parse_country_file('australia')
        self.assertIn(1990, parsed['years'])
        self.assertIn(17.3, parsed['populations'])
        self.assertIn(5.52, parsed['pollution'])

