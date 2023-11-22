"""
This file performs all the operations mentioned in readme for weather man problem
"""
import csv
import os
from datetime import datetime

def parse_weather_data(weather_row) -> dict:
    """
    parse the weather columns to respective data types
    """
    parsed_weather_row={}
    for key,value in weather_row.items():
        if key in ('PKT','PKST'):
            parsed_weather_row['PKT'] = datetime.strptime(value,"%Y-%m-%d")
        elif key ==' Events':
            parsed_weather_row[key.strip()]=value
        else:
            parsed_weather_row[key.strip()] = 0.0 if value=='' else float(value)
    return parsed_weather_row

def read_weather_data() -> list:
    """
    Read the data files from weatherfiles folder and return it
    """
    weather_data_dir=os.path.join(os.path.dirname(__file__),'weatherfiles')
    data_files=list(os.listdir(weather_data_dir))
    weather_data=[]
    for file_path in data_files:
        with open(os.path.join(weather_data_dir,file_path),'r',encoding='latin-1') as f:
            #replace null values with empty string
            csv_reader = csv.DictReader(x.replace('\0', '') for x in f) 
            for row in csv_reader:
                weather_row=parse_weather_data(row)
                weather_data.append(weather_row)
    return weather_data


print(read_weather_data())
