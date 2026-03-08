import json, os, time
import paho.mqtt.client as mqtt
import psycopg2

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
DB_HOST   = os.getenv("DB_HOST", "postgres")
DB_NAME   = os.getenv("DB_NAME", "zigbee_db")
DB_USER   = os.getenv("DB_USER", "zigbee_user")
DB_PASS   = os.getenv("DB_PASSWORD", "zigbee_pass")


def get_db():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def get_connection(userdata):
    conn = userdata.get("db")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        return conn
    except Exception:
        print("🔄 DB reconnecting...")
        try:
            conn.close()
        except Exception:
            pass
        new_conn = get_db()
        userdata["db"] = new_conn
        return new_conn


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
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
        """)
    conn.commit()
    print("✅ DB schema ready")


def on_connect(client, userdata, flags, rc, *args):
    if rc == 0:
        print("✅ Connected to MQTT broker")
        result, mid = client.subscribe("zigbee2mqtt/#")
        print(f"📡 Subscribed to zigbee2mqtt/# — result={result} mid={mid}")
    else:
        print(f"❌ MQTT connect failed rc={rc}")


def on_disconnect(client, userdata, flags, rc, *args):
    print(f"⚠️ Disconnected from MQTT rc={rc} — will auto-reconnect")


def on_subscribe(client, userdata, mid, granted_qos, *args):
    print(f"✅ Subscription confirmed mid={mid} qos={granted_qos}")


def on_message(client, userdata, msg):
    topic = msg.topic
    if "bridge" in topic:
        return
    try:
        payload = json.loads(msg.payload.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return

    parts = topic.split("/")
    if len(parts) < 2:
        return
    device_name = parts[1]

    print(f"📨 Message from '{device_name}': {payload}")

    conn = get_connection(userdata)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sensor_readings
                    (device_name, soil_moisture, humidity, temperature,
                     battery, linkquality, dry, raw)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                device_name,
                payload.get("soil_moisture"),
                payload.get("humidity"),
                payload.get("temperature"),
                payload.get("battery"),
                payload.get("linkquality"),
                payload.get("dry"),
                json.dumps(payload),
            ))
        conn.commit()
        print(f"💾 Saved: soil={payload.get('soil_moisture')} "
              f"humidity={payload.get('humidity')} "
              f"temp={payload.get('temperature')}")
    except Exception as e:
        print(f"❌ DB error: {e}")
        conn.rollback()


def main():
    print("⏳ Waiting for services to start...")
    time.sleep(8)

    conn = None
    while conn is None:
        try:
            conn = get_db()
            init_db(conn)
        except Exception as e:
            print(f"⏳ Waiting for DB... {e}")
            time.sleep(3)

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="zigbee_worker",
        userdata={"db": conn}
    )
    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe  = on_subscribe
    client.on_message    = on_message

    # Auto-reconnect: wait 1s min, 10s max between retries
    client.reconnect_delay_set(min_delay=1, max_delay=10)

    print(f"🔌 Connecting to MQTT at {MQTT_HOST}:{MQTT_PORT}")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()  # handles reconnects automatically


if __name__ == "__main__":
    main()
