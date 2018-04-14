import json
import datetime
from time import sleep
import pycurl
import io
import os
import codecs

# set constant
curl = pycurl.Curl()
url_base = 'http://api.aitc.jp/jmardb-api/search'
str_date_format = '%Y-%m-%d'
str_date_format_log = '%Y-%m-%d %H:%M:%S'
str_start = '2013-01-01'
str_useragent = 'Mozilla/5.0'
flg_debug = 1

# set def
def get_content(c, u):
    buffer = io.BytesIO()

    c.setopt(pycurl.URL, u)
    c.setopt(pycurl.USERAGENT, str_useragent)
    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)

    try:
        c.perform()

    except Exception as e:
        print(str(e))

    return buffer.getvalue()

# today
date_today = datetime.datetime.now()

# start day
date_start = datetime.datetime.strptime(str_start, str_date_format)

print('start')

# get JSON loop
while date_start < date_today:

    date_next = date_start + datetime.timedelta(days=1)

    url_json = url_base \
        + '?datetime=' + datetime.datetime.strftime(date_start, str_date_format) \
        + '&datetime=' + datetime.datetime.strftime(date_next, str_date_format)

    print(datetime.datetime.strftime(datetime.datetime.now(), str_date_format) + ' > ' + url_json)

    flg_next = True
    while flg_next is True:
        flg_next = False
        dict_json = json.loads(get_content(curl, url_json))

        # JSON loop
        for str_contents_key, contents in dict_json.items():
            # contents
            if str(str_contents_key) == 'data':
                # contents is list
                for dict_entry in contents:
                    # entries
                    for str_entry_key, str_entry_value in dict_entry.items():
                        # entry
                        if str(str_entry_key) == 'link':
                            url_xml = str(str_entry_value)

                            # get XML
                            str_filename = os.path.basename(url_xml) + '.xml'

                            if os.path.exists(str_filename) is False:
                                str_xml = get_content(curl, url_xml).decode('utf-8')

                                file = codecs.open(str_filename, 'w', 'utf-8')
                                file.write(str_xml)
                                file.close()
                            else:
                                print('file exists.')

            sleep(0.3)

            if str(str_contents_key) == 'paging':
                # contents is dictionary
                for str_paging_key, str_paging_value in contents.items():
                    # paging
                    if str(str_paging_key) == 'next':
                        url_json = str_paging_value
                        flg_next = True
                        print(datetime.datetime.strftime(datetime.datetime.now(), str_date_format) + ' > ' + url_json)
                        sleep(1)

    # slide days
    date_start = date_next

    # debug
    if flg_debug == 1:
       break

print('end')

exit()