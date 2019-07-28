Firstly activate the virtualenv
```
source venv/bin/activate
```
then migrate the models
```
python manage.py migrate --database=btc_db
python manage.py migrate --database=warehouse_db
```
- to load the data to a Database table
```
python manage.py import_from_csv
```
- To handle the scheduled tasks we can use celery. We can start a beat and a worker and will use redis server as message broker of celery
```
celery -A tele beat -l info
celery -A tele worker -l info
```
There is a task which will be triggered at 12:00 am(UTC) time

- There is also a web server which serves dashboard which contains yearly, monthly, daily data

- There is a notebook in which weighted price prediction model is developed by **ARIMA**

- It can be the architectural view of Business Intelligence and anamoly detection pipeline
  ![alt diagram](https://github.com/shourav9884/tele-test/raw/master/static/img/Untitled%20Diagram.jpg)
 