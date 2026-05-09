import os
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import datetime
import psycopg2
import pandas as pd
import uuid

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "zigbee_db")
DB_USER = os.getenv("DB_USER", "zigbee_user")
DB_PASS = os.getenv("DB_PASSWORD", "zigbee_pass")

def pandaSQL(sql_statement) -> pd.DataFrame:
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    df = pd.read_sql(sql_statement, conn)

    conn.close()
    return df

def sql(statement_command):
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    with conn.cursor() as cur:
            cur.execute(statement_command)
    conn.close()

def simulatedStatement():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    id = uuid.uuid4()
    device_name = f"device_{id}" 
    with conn.cursor() as cur:
        cur.execute("INSERT INTO sensor_readings (device_name, ts, soil_moisture, humidity, temperature, battery, linkquality, dry, raw) SELECT %s AS device_name, ts, round((random() * 50 + 10)::numeric, 2), round((random() * 40 + 30)::numeric, 2), round((random() * 170 - 20)::numeric, 2), (random() * 40 + 60)::int, (random() * 100)::int, (random() > 0.7), jsonb_build_object('simulated', true, 'note', 'generated sample') FROM generate_series('2026-01-01'::timestamptz, '2026-01-31 23:00:00'::timestamptz, interval '2 hours') AS gs(ts)", (device_name,))
    conn.commit()
    conn.close()

