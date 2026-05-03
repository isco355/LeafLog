import os
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import datetime
import psycopg2
import pandas as pd

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
    with conn.cursor() as cur:
            cur.execute(statement_command)
    conn.commit()


