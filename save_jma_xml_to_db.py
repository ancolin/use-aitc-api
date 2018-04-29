import os
import codecs
import psycopg2
from pathlib import Path
from xml.etree.ElementTree import *

# set constant
str_dbhost = os.getenv('PG_HOST', '127.0.0.1')
str_dbuser = os.getenv('PG_USER', 'postgres')
str_dbpass = os.getenv('PG_PASS', '')
str_dbinfo = 'dbname=jma-xml' \
    + ' host=' + str_dbhost \
    + ' user=' + str_dbuser \
    + ' password=' + str_dbpass
insert_d_xml = 'insert into d_xml values (%s, %s)'
insert_d_xml_header = 'insert into d_xml_header values (%s, %s, %s, %s)'
insert_d_xml_data_advisory = 'insert into d_xml_data_advisory values (%s, %s)'

list_years = range(2013, 2019)
list_months = range(1, 13)
list_days = range(1, 32)

dict_namespace = {
    'jmx': 'http://xml.kishou.go.jp/jmaxml1/'
    , 'jmx_ib': 'http://xml.kishou.go.jp/jmaxml1/informationBasis1/'
    , 'jmx_mete': 'http://xml.kishou.go.jp/jmaxml1/body/meteorology1/'
}

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
                            fp = None
                            data = None
                            try:
                                fp = codecs.open(str(file), 'r', 'utf-8')
                                data = fp.read()
                                fp.close()

                                data = data.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
                                                    , '<?xml version="1.0" encoding="UTF-8"?>')

                                elem = fromstring(data)
                                report_date_time = elem.find('./jmx_ib:Head/jmx_ib:ReportDateTime', dict_namespace).text
                                control_title = elem.find('./jmx:Control/jmx:Title', dict_namespace).text
                                head_infokind = elem.find('./jmx_ib:Head/jmx_ib:InfoKind', dict_namespace).text

                                cur.execute(insert_d_xml, (
                                    str(file), str(data)))
                                cur.execute(insert_d_xml_header, (
                                    str(file), str(control_title), str(head_infokind), str(report_date_time)))
                                conn.commit()

                                if control_title == '気象特別警報・警報・注意報' and head_infokind == '気象警報・注意報':
                                    list_information = elem.findall('./jmx_ib:Head//jmx_ib:Information', dict_namespace)

                                    for information in list_information:
                                        if information.get('type') != '気象警報・注意報（警報注意報種別毎）':
                                            codes = information.findall('.//jmx_ib:Area/jmx_ib:Code', dict_namespace)

                                            for code in codes:
                                                try:
                                                    cur.execute(insert_d_xml_data_advisory, (
                                                        str(file), str(code.text)))
                                                except Exception as e:
                                                    conn.rollback()

                                    conn.commit()

                            except Exception as e:
                                #print(e)
                                conn.rollback()
                                #exit()

                            del fp
                            del data

print('end')

exit()
