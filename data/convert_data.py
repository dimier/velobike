# coding: utf-8
import re
import csv
import sys

# Пример входных данных:
# ID клиента,Date of Start,Date of Finish,Start,Finish,Bike ID,Dur (time),Dur,Цена,Тип договора,Rush,Trz,H,Day
# 17296,31/10/14 16:47,31/10/14 19:41,14,7,V075,2:53:50,"2,8972","300,0",day,0,1,16,6

# Запуск:
# python convert_data.py < data_14.raw.csv > data_14.csv


dt_re = re.compile('(\d{1,2})/(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{1,2})')


reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', lineterminator='\n')
header = True
for row in reader:
    if header:
        writer.writerow(['dt', 'f', 't', 'l', 'd'])
        header = False
        continue

    duration = float(row[7].replace(',', '.'))
    if duration < 0 or duration >= 24:
        sys.stderr.write("skip\n")
        continue

    match = dt_re.match(row[1])
    if not match:
        sys.stderr.write('{}\n'.format(dt_re))
        break

    (day, month, year, hour, minute) = match.groups()
    if len(year) == 2:
        year = '20'+year

    dt = '{}{:02d}{:02d}{:02d}'.format(year, int(month), int(day), int(hour))

    writer.writerow([dt, '{:03d}'.format(int(row[3])), '{:03d}'.format(int(row[4])), int(round(duration)), 0])
