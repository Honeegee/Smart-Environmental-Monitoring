from web3 import Web3
import pandas as pd
import numpy as np

# Connect to Ethereum node (user should replace with their provider URL)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Default Ganache URL

# Load contract ABI and address (user should replace with actual values)
contract_address = '0x0f35F277FF0087f1e37d57611AEbD601fbA5FB2a'
contract_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "deviceId",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "dataType",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "dataValue",
				"type": "string"
			}
		],
		"name": "DataStored",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_deviceId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_dataType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_dataValue",
				"type": "string"
			}
		],
		"name": "storeData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "dataRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "deviceId",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "dataType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "dataValue",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getRecord",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalRecords",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "MAX_ENTRIES",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def retrieve_and_process_data():
    # Get total records
    total_records = contract.functions.getTotalRecords().call()
    print(f"Total IoT records stored: {total_records}")

    # Retrieve all IoT records
    data = []
    for i in range(total_records):
        record = contract.functions.getRecord(i).call()
        
        # Parse the data_value to extract original timestamp and value
        data_value = record[3]
        if "|" in data_value:
            original_timestamp, actual_value = data_value.split("|", 1)
        else:
            # Fallback to blockchain timestamp if no original timestamp
            original_timestamp = pd.to_datetime(record[0], unit="s").strftime("%Y-%m-%d %H:%M:%S")
            actual_value = data_value
        
        data.append({
            "timestamp": original_timestamp,
            "device_id": record[1],
            "data_type": record[2],
            "data_value": actual_value
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Convert timestamp to datetime (it's already in string format from CSV)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Extract numeric values from the actual sensor values
    df["numeric_value"] = df["data_value"].str.extract(r'(\d+\.?\d*)').astype(float)

    # Handle missing values
    if df.isnull().sum().sum() < len(df) * 0.1:  # If less than 10% missing
        df.fillna(0, inplace=True)
    else:
        # Use mean/median based on data type
        for col in df.select_dtypes(include=['float64']):
            df[col].fillna(df[col].median(), inplace=True)

    # Save to CSV
    df.to_csv("cleaned_iot_data.csv", index=False)
    print("✅ Cleaned IoT data saved successfully as cleaned_iot_data.csv")

    return df

if __name__ == "__main__":
    df = retrieve_and_process_data()
    print(df.head())
