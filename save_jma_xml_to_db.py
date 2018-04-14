import os
import codecs
import psycopg2
from pathlib import Path

# set constant
str_dbhost = os.getenv('PG_HOST', '127.0.0.1')
str_dbuser = os.getenv('PG_USER', 'postgres')
str_dbpass = os.getenv('PG_PASS', '')
str_dbinfo = 'dbname=jma-xml' \
    + ' host=' + str_dbhost \
    + ' user=' + str_dbuser \
    + ' password=' + str_dbpass
sql = 'insert into d_xml values (%s, %s)'

list_years = range(2013, 2019)
list_months = range(1, 13)
list_days = range(1, 32)

print('start')

# connect database
with psycopg2.connect(str_dbinfo) as conn:
    with conn.cursor() as cur:

        # file loop
        files = Path('data')
        for year in list_years:
            year = '{0:04d}'.format(year)
            for month in list_months:
                month = '{0:02d}'.format(month)
                for day in list_days:
                    day = '{0:02d}'.format(day)
                    path = year + '/' + month + '/' + day
                    if os.path.exists('data/' + path) is True:
                        print(path)
                        for file in files.glob(path + '/*.xml'):
                            try:
                                xml = codecs.open(str(file), 'r', 'utf-8')
                                data = xml.read()
                                xml.close()

                                cur.execute(sql, (str(file), str(data)))
                                conn.commit()
                            except Exception as e:
                                conn.rollback()

print('end')

exit()
