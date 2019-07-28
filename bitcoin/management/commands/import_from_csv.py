import csv

from django.core.management import BaseCommand
from django.db import connections


class Command(BaseCommand):

    def insert_to_db(self, records):
        # print(records)
        with connections['btc_db'].cursor() as cursor:
            sql_insert_query = """ INSERT INTO btc_data (btc_timestamp,opening_value,closing_value,high_value,low_value,volumne_in_btc,volumne_in_currency,weighted_price) 
                                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """

            result = cursor.executemany(sql_insert_query, records)
            connections['btc_db'].commit()

    def handle(self, *args, **options):
        # print("kkkk")
        fp = open('bitstampUSD_1-min_data_2012-01-01_to_2019-03-13.csv', 'r')
        data_reader = csv.reader(fp, delimiter=',', quotechar='"')
        #
        buffered_data = []
        count = 0
        started=False
        # yield next(data_reader)
        r_count = 0
        for row in data_reader:
            if started:
                i=0
                for data in row:
                    if data == 'NaN':
                        row[i]=None
                    i=i+1

                buffered_data.append(
                    row
                )
                # if count == 100000:
                #     self.insert_to_db(buffered_data)
                #     buffered_data = []
                #     count = 0
                #     print(r_count)

                count += 1
                r_count += 1

            started = True
        self.insert_to_db(buffered_data)


