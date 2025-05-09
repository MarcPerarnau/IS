import json
import mysql.connector
from datetime import datetime

LOG_FILE = "/var/log/suricata/eve.json"

db = mysql.connector.connect(
    host="localhost",
    user="superiron",
    password="tu_contraseña",
    database="ironshield"
)
cursor = db.cursor()

def procesar_log():
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("event_type") == "alert":
                    ip_src = data.get("src_ip", "")
                    ip_dst = data.get("dest_ip", "")
                    tipo = data["alert"]["signature"]
                    fecha = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")

                    cursor.execute("""
                        INSERT INTO logs (ip_src, ip_dst, tipo_evento, fecha)
                        VALUES (%s, %s, %s, %s)
                    """, (ip_src, ip_dst, tipo, fecha))
                    db.commit()
            except Exception as e:
                print("Error al procesar línea:", e)

procesar_log()
