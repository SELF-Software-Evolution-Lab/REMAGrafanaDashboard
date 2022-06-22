import random
from xmlrpc.client import DateTime
import psycopg2
from datetime import datetime
import time

data = []
with open("datos-historicos-iot.csv", "r") as f:
    for x in f.readlines()[1:]:
        data.append(x.replace("\n","")) 
conn = psycopg2.connect(
        host="grafanadb.czgvwdloohn6.us-east-1.rds.amazonaws.com",
        database="proyectoGrado1",
        user="grafana",
        password="grafana10"
    )
cur = conn.cursor()
while(True):    
    comoseledelagana = random.choice(data)
    columnas = str(comoseledelagana).split(",")      
    sql = """INSERT INTO \"iotHistorico\" (\"Usuario\", \"Ciudad\", \"Fecha\",\"Variable\", \"Medicion\") VALUES (%s,%s,%s,%s,%s) """
    cur.execute(sql, (columnas[0], columnas[1], datetime.now(), columnas[3], columnas[4] ))
    conn.commit()
    time.sleep(1)
conn.close()