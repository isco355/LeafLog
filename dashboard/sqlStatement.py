

CREATE_TABLE_SENSOR_READING=""" CREATE TABLE IF NOT EXISTS sensor_readings (
                id            SERIAL PRIMARY KEY,
                device_name   TEXT        NOT NULL,
                ts            TIMESTAMPTZ DEFAULT NOW(),
                soil_moisture FLOAT,
                humidity      FLOAT,
                temperature   FLOAT,
                battery       INTEGER,
                linkquality   INTEGER,
                dry           BOOLEAN,
                raw           JSONB
            );
            CREATE INDEX IF NOT EXISTS idx_ts        ON sensor_readings (ts DESC);
            CREATE INDEX IF NOT EXISTS idx_device_ts ON sensor_readings (device_name, ts DESC);
"""




CREATE_TABLE_DEVICE="""CREATE TABLE IF NOT EXISTS devices (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id INTEGER NOT NULL,
    device_name TEXT NOT NULL
);"""
