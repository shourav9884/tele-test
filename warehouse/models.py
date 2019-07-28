from datetime import datetime

from django.db import models

# Create your models here

class ReportByDay(models.Model):
    day_start_time = models.BigIntegerField()
    day_minimum_time = models.BigIntegerField(null=True)
    day_maximum_time = models.BigIntegerField(null=True)
    sum_opening_value = models.FloatField(null=True)
    max_opening_value = models.FloatField(null=True)
    min_opening_value = models.FloatField(null=True)
    sum_closing_value = models.FloatField(null=True)
    max_closing_value = models.FloatField(null=True)
    min_closing_value = models.FloatField(null=True)
    max_high_value = models.FloatField(null=True)
    min_high_value = models.FloatField(null=True)
    max_low_value = models.FloatField(null=True)
    min_low_value = models.FloatField(null=True)
    sum_volumne_in_btc = models.FloatField(null=True)
    max_volumne_in_btc = models.FloatField(null=True)
    min_volumne_in_btc = models.FloatField(null=True)
    sum_volumne_in_currency = models.FloatField(null=True)
    max_volumne_in_currency = models.FloatField(null=True)
    min_volumne_in_currency = models.FloatField(null=True)
    sum_weighted_price = models.FloatField(null=True)
    max_weighted_price = models.FloatField(null=True)
    min_weighted_price = models.FloatField(null=True)
    row_count = models.IntegerField(default=0)

    def start_time(self):
        return datetime.fromtimestamp(self.day_start_time).strftime("%d-%m-%Y")

    def avg_price(self):
        maximum = self.max_weighted_price if self.max_weighted_price else 0
        minimum = self.min_weighted_price if self.min_weighted_price else 0
        return (maximum+minimum)/2


class ReportByMonth(models.Model):
    month_start_time = models.BigIntegerField()
    month_minimum_time = models.BigIntegerField(null=True)
    month_maximum_time = models.BigIntegerField(null=True)
    sum_opening_value = models.FloatField(null=True)
    max_opening_value = models.FloatField(null=True)
    min_opening_value = models.FloatField(null=True)
    sum_closing_value = models.FloatField(null=True)
    max_closing_value = models.FloatField(null=True)
    min_closing_value = models.FloatField(null=True)
    max_high_value = models.FloatField(null=True)
    min_high_value = models.FloatField(null=True)
    max_low_value = models.FloatField(null=True)
    min_low_value = models.FloatField(null=True)
    sum_volumne_in_btc = models.FloatField(null=True)
    max_volumne_in_btc = models.FloatField(null=True)
    min_volumne_in_btc = models.FloatField(null=True)
    sum_volumne_in_currency = models.FloatField(null=True)
    max_volumne_in_currency = models.FloatField(null=True)
    min_volumne_in_currency = models.FloatField(null=True)
    sum_weighted_price = models.FloatField(null=True)
    max_weighted_price = models.FloatField(null=True)
    min_weighted_price = models.FloatField(null=True)
    row_count = models.IntegerField(default=0)

    def start_time(self):
        return datetime.fromtimestamp(self.month_start_time).strftime("%d-%m-%Y")

    def avg_price(self):
        maximum = self.max_weighted_price if self.max_weighted_price else 0
        minimum = self.min_weighted_price if self.min_weighted_price else 0
        return (maximum+minimum)/2

