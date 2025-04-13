from django.test import TestCase
from django.apps import apps
from countries.apps import CountriesConfig

def test_app_config_name():
    assert CountriesConfig.name == 'countries'

def test_app_is_registered():
    app_config = apps.get_app_config('countries')
    assert isinstance(app_config, CountriesConfig)

