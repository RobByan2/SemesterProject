
# Get Data

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import os

#Personal API key
api_key = 'c5390e8aa2454561b4b1f89bf1e62d0e'

#BLS IDs
api_data = ["CES0000000001", #Total Nonfarm Employment
            "LNS14000000", #Unemployment Rate
            "PRS85006092", #Output Per Hour - Non-farm Business Productivity
            "PRS85006112", #Nonfarm Business Unit Labor Costs
            "EIUIR", #Imports
            "EIUIQ" #Exports
            ]

#Folder to save CSV files
output_dir = 'bls_data_files'
os.makedirs(output_dir, exist_ok=True)


# File names for storing data
file_names = {
    "CES0000000001": os.path.join(output_dir, "Total_Nonfarm_Employment.csv"),
    "LNS14000000": os.path.join(output_dir, "Unemployment_Rate.csv"),
    "PRS85006092": os.path.join(output_dir, "Output_Per_Hour.csv"),
    "PRS85006112": os.path.join(output_dir, "Nonfarm_Business_Unit_Labor_Costs.csv"),
    "EIUIR": os.path.join(output_dir, "Imports.csv"),
    "EIUIQ": os.path.join(output_dir, "Exports.csv")
}

#Retrieve the data from BLS
def collect_data(api_key, api_data):
    headers = {'Content-type': 'application/json'}
    current_year = datetime.now().year
    start_year = current_year - 9
    data = json.dumps({
        "seriesid": api_data,
        "startyear": str(start_year),
        "endyear": str(current_year),
        "registrationkey": api_key
    })
    response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', headers=headers, data=data)
    json_data = response.json()

    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        series_data = []
        for item in series['data']:
            series_data.append([item['year'], item['period'], item['value']])
        df = pd.DataFrame(series_data, columns=['Year', 'Period', 'Value'])
        df.to_csv(file_names[series_id], index=False)

def load_data(file_names):
    data_frames = {}
    for series_id, file_name in file_names.items():
        data_frames[series_id] = pd.read_csv(file_name)
    return data_frames

# Collect data and store it
collect_data(api_key, api_data)

# Load data
data_frames = load_data(file_names)
