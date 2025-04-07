from django.db import models

class CountryData(models.Model):
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    population_mil = models.FloatField()
    pollution_affected_mil = models.FloatField()

    def __str__(self):
        return f'{self.year} - {self.country} - Population: {self.population_mil}M, Population Affected by Pollution: {self.pollution_affected_mil}M'