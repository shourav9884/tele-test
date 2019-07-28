from __future__ import absolute_import

import logging
from datetime import datetime, timedelta
import calendar

import psycopg2
from celery.schedules import crontab
from django.db import connections
from django.db.models import Sum, Max, Min, Count
from django.utils.timezone import now

from bitcoin.models import BitcoinData
from warehouse.models import ReportByDay, ReportByMonth
from tele.celery import app as celery_app

logger = logging.getLogger('django')

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=10, minute=31), prev_day_data.s())


def import_day_data(day):
    try:
        from_time = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=0,
            minute=1
        )

        next_day = day + timedelta(days=1)
        to_time = datetime(
            year=next_day.year,
            month=next_day.month,
            day=next_day.day,
            hour=0,
            minute=0
        )
        from_time = int((from_time - datetime(1970, 1, 1)).total_seconds())
        to_time = int((to_time - datetime(1970, 1, 1)).total_seconds())

        db_data = BitcoinData.objects.filter(btc_timestamp__gte=from_time, btc_timestamp__lte=to_time).aggregate(
            Sum('opening_value'),
            Max('opening_value'),
            Min('opening_value'),
            Sum('closing_value'),
            Max('closing_value'),
            Min('closing_value'),
            Max('btc_timestamp'),
            Min('btc_timestamp'),
            Max('high_value'),
            Min('high_value'),
            Max('low_value'),
            Min('low_value'),
            Sum('volumne_in_btc'),
            Max('volumne_in_btc'),
            Min('volumne_in_btc'),
            Sum('volumne_in_currency'),
            Max('volumne_in_currency'),
            Min('volumne_in_currency'),
            Sum('weighted_price'),
            Max('weighted_price'),
            Min('weighted_price'),
            Count('btc_timestamp')
        )

        report_by_day = []
        old_report = ReportByDay.objects.filter(day_start_time=from_time).first()
        if old_report:
            old_report.delete()
        ReportByDay.objects.create(
            day_start_time=from_time,
            day_minimum_time=db_data['btc_timestamp__min'],
            day_maximum_time=db_data['btc_timestamp__min'],
            sum_opening_value=db_data['opening_value__sum'],
            max_opening_value=db_data['opening_value__max'],
            min_opening_value=db_data['opening_value__min'],
            sum_closing_value=db_data['closing_value__sum'],
            max_closing_value=db_data['closing_value__max'],
            min_closing_value=db_data['closing_value__min'],
            max_high_value=db_data['high_value__max'],
            min_high_value=db_data['high_value__min'],
            max_low_value=db_data['low_value__max'],
            min_low_value=db_data['low_value__min'],
            sum_volumne_in_btc=db_data['volumne_in_btc__sum'],
            max_volumne_in_btc=db_data['volumne_in_btc__max'],
            min_volumne_in_btc=db_data['volumne_in_btc__min'],
            sum_volumne_in_currency=db_data['volumne_in_currency__sum'],
            max_volumne_in_currency=db_data['volumne_in_currency__max'],
            min_volumne_in_currency=db_data['volumne_in_currency__min'],
            sum_weighted_price=db_data['weighted_price__sum'],
            max_weighted_price=db_data['weighted_price__max'],
            min_weighted_price=db_data['weighted_price__min'],
            row_count=db_data['btc_timestamp__count']

        )
        # i = 1/0

    except Exception as e:
        logger.exception(msg="error in import_day_data for day: {day}, at:{now}".format(day=day, now=now()))
        # print(e)


def import_month_data(month):
    last_day_month = calendar.monthrange(month.year, month.month)[1]
    from_time = datetime(
        year=month.year,
        month=month.month,
        day=1,
        hour=0,
        minute=1
    )

    next_month = month + timedelta(days=last_day_month)
    to_time = datetime(
        year=next_month.year,
        month=next_month.month,
        day=1,
        hour=0,
        minute=0
    )

    from_time = int((from_time - datetime(1970, 1, 1)).total_seconds())
    to_time = int((to_time - datetime(1970, 1, 1)).total_seconds())

    db_data = BitcoinData.objects.filter(btc_timestamp__gte=from_time, btc_timestamp__lte=to_time).aggregate(
        Sum('opening_value'),
        Max('opening_value'),
        Min('opening_value'),
        Sum('closing_value'),
        Max('closing_value'),
        Min('closing_value'),
        Max('btc_timestamp'),
        Min('btc_timestamp'),
        Max('high_value'),
        Min('high_value'),
        Max('low_value'),
        Min('low_value'),
        Sum('volumne_in_btc'),
        Max('volumne_in_btc'),
        Min('volumne_in_btc'),
        Sum('volumne_in_currency'),
        Max('volumne_in_currency'),
        Min('volumne_in_currency'),
        Sum('weighted_price'),
        Max('weighted_price'),
        Min('weighted_price'),
        Count('btc_timestamp')
    )

    old_report = ReportByMonth.objects.filter(month_start_time=from_time).first()
    if old_report:
        old_report.delete()
    ReportByMonth.objects.create(
        month_start_time=from_time,
        month_minimum_time=db_data['btc_timestamp__min'],
        month_maximum_time=db_data['btc_timestamp__min'],
        sum_opening_value=db_data['opening_value__sum'],
        max_opening_value=db_data['opening_value__max'],
        min_opening_value=db_data['opening_value__min'],
        sum_closing_value=db_data['closing_value__sum'],
        max_closing_value=db_data['closing_value__max'],
        min_closing_value=db_data['closing_value__min'],
        max_high_value=db_data['high_value__max'],
        min_high_value=db_data['high_value__min'],
        max_low_value=db_data['low_value__max'],
        min_low_value=db_data['low_value__min'],
        sum_volumne_in_btc=db_data['volumne_in_btc__sum'],
        max_volumne_in_btc=db_data['volumne_in_btc__max'],
        min_volumne_in_btc=db_data['volumne_in_btc__min'],
        sum_volumne_in_currency=db_data['volumne_in_currency__sum'],
        max_volumne_in_currency=db_data['volumne_in_currency__max'],
        min_volumne_in_currency=db_data['volumne_in_currency__min'],
        sum_weighted_price=db_data['weighted_price__sum'],
        max_weighted_price=db_data['weighted_price__max'],
        min_weighted_price=db_data['weighted_price__min'],
        row_count=db_data['btc_timestamp__count']

    )

def backpop_day(from_day, to_day):
    day_timestamp = from_day
    while day_timestamp <= to_day:
        day = datetime.utcfromtimestamp(day_timestamp)
        import_day_data(day)
        day_timestamp = day_timestamp + 24 * 60 * 60


def backpop_month(from_month, to_month):
    month_timestamp = from_month
    while month_timestamp <= to_month:
        month = datetime.utcfromtimestamp(month_timestamp)
        import_month_data(month)
        last_day_month = calendar.monthrange(month.year, month.month)[1]
        month_timestamp = month_timestamp + last_day_month * 24 * 60 * 60


def backpop(from_time=0, to_time=None):
    if not to_time:
        to_time = datetime.utcnow()
        to_time = int((to_time - datetime(1970, 1, 1)).total_seconds())
    max_time = BitcoinData.objects.filter(btc_timestamp__lte=to_time).aggregate(Max('btc_timestamp'))
    to_time = max_time['btc_timestamp__max']
    min_time = BitcoinData.objects.filter(btc_timestamp__gte=from_time).aggregate(Min('btc_timestamp'))
    from_time = min_time['btc_timestamp__min']

    backpop_day(from_time, to_time)
    backpop_month(from_time, to_time)


@celery_app.task()
def prev_day_data():
    now_time = datetime.utcnow()
    previous_day = now_time - timedelta(days=1)
    import_day_data(previous_day)
    if now_time.month != previous_day.month:
        import_month_data(previous_day)
