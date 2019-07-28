import calendar
from datetime import datetime, timedelta

from django.db import connections
from django.shortcuts import render

# Create your views here.
from warehouse.models import ReportByDay, ReportByMonth


def dashboard(request):
    now_time = datetime.now()
    now_time = datetime(
        year=now_time.year,
        month=4,
        day=1
    )
    prev_month = datetime(
        year=now_time.year,
        month=now_time.month-1,
        day=1
    )
    last_day_month = calendar.monthrange(prev_month.year, prev_month.month)[1]
    daily_data_from_time = prev_month
    prev_month_last_day = prev_month + timedelta(days=last_day_month)
    daily_data_to_time = prev_month_last_day
    prev_month = int((prev_month - datetime(1970, 1, 1)).total_seconds())
    prev_month_last_day = int((prev_month_last_day - datetime(1970, 1, 1)).total_seconds())

    daily_data = ReportByDay.objects.filter(day_start_time__gte=prev_month, day_maximum_time__lte=prev_month_last_day)

    prev_year = datetime(
        year=daily_data_to_time.year-1,
        month=daily_data_to_time.month,
        day=daily_data_to_time.day
    )

    monthly_data_from_time = prev_year
    prev_year = int((prev_year - datetime(1970, 1, 1)).total_seconds())
    monthly_data_to_time = daily_data_to_time
    prev_year_last_day = int((monthly_data_to_time - datetime(1970, 1, 1)).total_seconds())

    monthly_data = ReportByMonth.objects.filter(month_start_time__gte=prev_year, month_start_time__lte=prev_year_last_day)

    cursor = connections['warehouse_db'].cursor()
    cursor.execute("select avg((max_weighted_price+min_weighted_price)/2),extract(year from to_timestamp(month_start_time)) as year from warehouse_reportbymonth group by year order by year ");
    yearly_data = cursor.fetchall();

    return render(request, 'dashboard.html', locals())