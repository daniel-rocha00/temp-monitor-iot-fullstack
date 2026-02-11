import paho.mqtt.client as mqtt
import json
import sqlite3


connection = sqlite3.connect("../data/sensor-data.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensors(
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        sensorName TEXT, value REAL
        )               

''')

def commitSQL(id, temperatura):
    cursor.execute(
        "INSERT INTO sensors(sensorName, value) VALUES (?, ?)", (id, temperatura)
    )
    connection.commit()

def JSONreader(client, userdata, msg):
    myJSON = msg.payload.decode()
    values = json.loads(myJSON)

    print(f"Temperatura recebida de {values["ID"]}: {values["temperatura"]}C")
    
    commitSQL(values["ID"], values["temperatura"])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = JSONreader
client.connect("localhost", 1883)
client.subscribe("sensores/cpp17")

print("Sistema pronto! Aguardando leituras...")
client.loop_forever()

connection.close

