import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


connection = sqlite3.connect("./data/sensor-data.db")
query = "SELECT timestamp, value, sensorName FROM sensors"
dataframe = pd.read_sql_query(query, connection)
connection.close

dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

dataframe['timestamp'] = dataframe['timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')

dataframe.set_index('timestamp', inplace=True)

sensorList = dataframe['sensorName'].unique()

plt.figure(figsize=(18, 9))

plt.title('Temperature by Hour', fontsize=24, pad=30)
plt.ylabel('Temperatures (°C)', fontsize=18, labelpad=24)
plt.xlabel('Timestamp', fontsize=18, labelpad=24)

plt.grid(True, alpha=0.5)

for sensor in sensorList:
    df_sensorReading = dataframe[dataframe['sensorName'] == sensor]

    plt.plot(df_sensorReading.index, df_sensorReading['value'], label=sensor, marker='o', linewidth=2, markersize=4)

plt.legend()

plt.gcf().autofmt_xdate()

graphName = './output/telemetry-chart.png'
plt.savefig(graphName, dpi=300, bbox_inches='tight')
print(f'Graph sucessfully saved as {graphName}!')
