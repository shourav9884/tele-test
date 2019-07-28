from django.db import models

# Create your models here.


class BitcoinData(models.Model):
    btc_timestamp = models.BigIntegerField()
    opening_value = models.FloatField(null=True)
    closing_value = models.FloatField(null=True)
    high_value = models.FloatField(null=True)
    low_value = models.FloatField(null=True)
    volumne_in_btc = models.FloatField(null=True)
    volumne_in_currency = models.FloatField(null=True)
    weighted_price = models.FloatField(null=True)

    class Meta:
        db_table = "btc_data"
        # app_label = "btc_db"