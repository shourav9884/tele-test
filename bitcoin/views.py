from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from bitcoin.models import BitcoinData


def test(request):
    result = BitcoinData.objects.raw('select count(*), extract(month from to_timestamp(btc_timestamp)) as month, extract(year from to_timestamp(btc_timestamp)) as year from btc_data group by year, month')