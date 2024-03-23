import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

log_file = "log_file2.txt" 
target_file = "transformed_data.csv" 

def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe

#columns: car_model,year_of_manufacture,price,fuel

def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(colums=["car_model",'year_of_manufacture','price','fuel'])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        car_model = person.find("car_model").text
        year_of_manufacture = float(person.find("year_of_manufacture").text)
        price = float(person.find("price").text)
        fuel =  float(person.find("fuel").text)
        dataframe = pd.concat([dataframe,pd.DataFrame([{'car_model':car_model,'year_of_manufacture':year_of_manufacture,'price':price,'fuel':fuel}])],ignore_index=True)
        return dataframe

def extract(): 
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price','fuel']) # create an empty data frame to hold extracted data 
     
    # process all csv files 
    for csvfile in glob.glob("*.csv"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True) 
         
    # process all json files 
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True) 
     
    # process all xml files 
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True) 
         
    return extracted_data 

def transform(data): 
    '''Round off to two decimals '''
    data['price'] = round(data.price,2) 
    data['fuel'] = round(data.fuel,2) 
    
    return data 

def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 

'''
To record the message, you need to implement a function log_progress() that accepts the log message as the argument. 
The function captures the current date and time using the datetime function from the datetime library. 
The use of this function requires the definition of a date-time format, 
and you need to convert the timestamp to a string format using the strftime attribute. 
'''

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp+","+message+"\n")

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 

