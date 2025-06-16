import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration for 100 records with 15-minute intervals
num_records = 100
interval_minutes = 15

# Generate sequential timestamps (15-minute intervals)
start_time = datetime.now() - timedelta(hours=25)  # Start 25 hours ago
timestamps = []
for i in range(num_records):  # Generate 100 timestamps
    timestamps.append(start_time + timedelta(minutes=i * interval_minutes))

# Device IDs - cycle through them
device_ids = ["ENV188", "ENV919", "ENV821", "ENV648"]

# Generate data directly in wide format for environmental_data.csv
environmental_data = []

for i, timestamp in enumerate(timestamps):
    device_id = device_ids[i % len(device_ids)]  # Cycle through devices
    
    # Generate realistic sensor values
    temperature = round(np.random.uniform(18.0, 35.0), 1)
    humidity = round(np.random.uniform(30.0, 85.0), 1)
    co2 = float(np.random.randint(350, 1500))
    air_quality = round(np.random.uniform(25.0, 450.0), 1)
    
    record = {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": device_id,
        "Temperature": temperature,
        "Humidity": humidity,
        "CO2": co2,
        "AirQuality": air_quality
    }
    environmental_data.append(record)

# Convert to DataFrame
df_wide = pd.DataFrame(environmental_data)

# Generate long format data for cleaned_iot_data.csv
long_data = []
for _, row in df_wide.iterrows():
    for sensor_type in ["Temperature", "Humidity", "CO2", "AirQuality"]:
        value = row[sensor_type]
        if sensor_type == "Temperature":
            data_value = f"{value}°C"
        elif sensor_type == "Humidity":
            data_value = f"{value}%"
        elif sensor_type == "CO2":
            data_value = f"{int(value)}ppm"
        else:  # AirQuality
            data_value = f"{value}"
        
        long_record = {
            "timestamp": row["timestamp"],
            "device_id": row["device_id"],
            "data_type": sensor_type,
            "data_value": data_value,
            "numeric_value": value
        }
        long_data.append(long_record)

df_long = pd.DataFrame(long_data)

# Save files
df_long.to_csv("cleaned_iot_data.csv", index=False)
df_wide.to_csv("environmental_data.csv", index=False)
df_long.to_json("environmental_data.json", orient="records")

# Display summary
print(f"Generated {len(df_wide)} environmental records with 15-minute intervals")
print(f"Generated {len(df_long)} long format records")
print(f"Time range: {df_wide['timestamp'].min()} to {df_wide['timestamp'].max()}")
print(f"Devices: {df_wide['device_id'].unique()}")
print("\nFirst few rows of environmental_data.csv:")
print(df_wide.head(10))
print(f"\nSaved to cleaned_iot_data.csv (Long format - {len(df_long)} records)")
print(f"Saved to environmental_data.csv (Wide format - {len(df_wide)} records)")
print(f"Saved to environmental_data.json")
