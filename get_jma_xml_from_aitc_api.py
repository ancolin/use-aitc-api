import json
import datetime
from time import sleep
import urllib.request
import os
import codecs


def get_content(u):
    res = ''
    try:
        res = urllib.request.urlopen(u).read()

    except Exception as e:
        print(str(e))

    return res


# set constant
url_base = 'http://api.aitc.jp/jmardb-api/search'
str_date_format = '%Y-%m-%d'
str_date_format_dir = '%Y/%m/%d'
str_date_format_log = '%Y-%m-%d %H:%M:%S'
str_start = '2013-01-01'

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
        + '&datetime=' + datetime.datetime.strftime(date_next, str_date_format) \
        + '&order=old&limit=50'

    print(datetime.datetime.strftime(datetime.datetime.now(), str_date_format) + ' > ' + url_json)

    dir_data = 'data/' + datetime.datetime.strftime(date_start, str_date_format_dir)
    os.makedirs(dir_data, exist_ok=True)

    flg_next = True
    while flg_next is True:
        flg_next = False
        dict_json = json.loads(get_content(url_json))

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
                            str_filename = dir_data + '/' + os.path.basename(url_xml) + '.xml'

                            if os.path.exists(str_filename) is False:
                                # create file
                                str_xml = get_content(url_xml).decode('utf-8')

                                file = codecs.open(str_filename, 'w', 'utf-8')
                                file.write(str_xml)
                                file.close()

                                sleep(0.3)

            if str(str_contents_key) == 'paging':
                # contents is dictionary
                for str_paging_key, str_paging_value in contents.items():
                    # paging
                    if str(str_paging_key) == 'next':
                        if str_paging_value is None:
                            continue
                        url_json = str_paging_value
                        flg_next = True
                        print(datetime.datetime.strftime(datetime.datetime.now()
                                                         , str_date_format) + ' > ' + url_json)

    # slide days
    date_start = date_next

print('end')

exit()
