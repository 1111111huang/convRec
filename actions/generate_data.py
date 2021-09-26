from typing import Dict, Text, Any, List, Union
import json
import pandas as pd
#use absolute path on your local here, somehow
data_file = open("C:/Users/huang/Documents/Tianqi Huang/Research/Thesis/Rasa/yelp_data/yelp_academic_dataset_business.json", encoding='utf-8')
data = []
for line in data_file:
    data.append(json.loads(line))
business_df = pd.DataFrame(data)
attributes=[]
for i in range(business_df.shape[0]):
    if(business_df.iloc[i].attributes!=None):
        attributes+=business_df.iloc[i].attributes.keys()
attributes = list(dict.fromkeys(attributes))
sentences=[]
for attribute in attributes:
    sentences+=["- I want " + attribute + " {\"entity\": \"preferences\", \"role\":  \"other\"} for better experience"]
textfile = open("sentences.txt", "w+")
for element in sentences:
    textfile.write(element + "\n")
textfile.close()