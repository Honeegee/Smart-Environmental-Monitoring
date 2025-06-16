import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_sensor_data():
    # Load cleaned IoT data
    df = pd.read_csv("../cleaned_iot_data.csv")
    
    # Verify data
    print("First few rows of data:")
    print(df.head())
    
    # Convert timestamp column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Set visualization style
    sns.set(style="whitegrid")
    
    # Create line plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        x=df["timestamp"],
        y=df["numeric_value"],
        hue=df["data_type"],
        marker="o"
    )
    
    # Format plot
    plt.xticks(rotation=45)
    plt.title("IoT Sensor Readings Over Time", fontsize=14)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Sensor Value", fontsize=12)
    plt.legend(title="Sensor Type")
    
    # Save plot
    plt.tight_layout()
    plt.savefig("sensor_readings_plot.png")
    print("Plot saved as sensor_readings_plot.png")
    
    # Display plot
    plt.show()

if __name__ == "__main__":
    visualize_sensor_data()
