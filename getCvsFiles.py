#!/usr/bin/env python
from __future__ import print_function

import pymysql
import os
import csv
import simplekml

fechas = ['2017-04-07%','2017-04-08%','2017-04-09%','2017-04-10%'
    , '2017-04-11%','2017-04-12%','2017-04-13%','2017-04-14%','2017-04-15%','2017-04-16%','2017-04-17%','2017-04-18%','2017-04-19%','2017-04-20%','2017-04-21%'
    , '2017-04-22%','2017-04-23%','2017-04-24%','2017-04-25%','2017-04-26%','2017-04-27%','2017-04-28%','2017-04-29%','2017-04-30%'
    , '2017-05-01%','2017-05-02%','2017-05-03%']
print( fechas[0] )
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='posiciones')

cur = conn.cursor()

cur.execute("SELECT distinct Name FROM posiiciones_rafael_nuno")

print(cur.description)

print()
autos = []
remove = set("(),")
for row in cur:
    autos.append(''.join(x for x in row if x not in remove))

for auto in autos:
    if not os.path.exists("rafael/"+auto.strip()):
        os.makedirs("rafael/"+auto.strip())

    for fecha in fechas:
        query_string = " SELECT *, CONCAT_WS(' Velocidad: ', Description_f,truncate( Velocidad_kH, 2 ) ) "+"AS Description FROM posiiciones_rafael_nuno" + " WHERE Name = '"+ auto +"' " + "AND Description_f LIKE '"+ fecha + "'; "
       # print(query_string)
        cur.execute( query_string )
        with open( "rafael/"+auto.strip()+"/"+fecha+".csv", "w", newline='') as csv_file:  # Python 3 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cur.description])  # write headers
            csv_writer.writerows(cur)

cur.close()
conn.close()