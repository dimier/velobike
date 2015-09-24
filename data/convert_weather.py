# coding: utf-8
import re
import csv
import sys

# Пример входных данных:
# Местное время в Санкт-Петербурге,T,Скорость ветра,WW
# 31.10.2014 21:00,3.0,2,Снег непрерывный слабый в срок наблюдения. 

# Запуск:
# python convert_weather.py < weather_14.raw.csv > weather_14.csv


dt_re = re.compile('(\d{1,2})\.(\d{1,2})\.(\d{1,4}) (\d{1,2}):(\d{1,2})')


reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', lineterminator='\n')
header = True
for row in reader:
    if header:
        writer.writerow(['dt', 'state', 'description_ru', 'description_en', 'temp'])
        header = False
        continue

    match = dt_re.match(row[0])
    if not match:
        sys.stderr.write('{}\n'.format(row[0]))
        break

    (day, month, year, hour, minute) = match.groups()
    if len(year) == 2:
        year = '20'+year

    if hour != '15':
        continue

    dt = '{}{:02d}{:02d}'.format(year, int(month), int(day))

    conditions = row[3].decode('utf8').lower()
    state = ''
    if u'дождь' in conditions or u'морось' in conditions or u'снег' in conditions:
        state = 'rain'

    writer.writerow([dt, state, row[3], row[3], row[1]])
