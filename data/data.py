import json
import pandas as pd


def recursively_clean_json(data):
    if data==False or data=="False":
        return None
    elif(type(data) is not dict):
        return data
    else:
        ret_val={}
        for key in data.keys():
            temp = recursively_clean_json(data[key])
            if temp is not None:
                ret_val[key]=temp
        return ret_val


data_file = open("../yelp_data/yelp_academic_dataset_business.json", encoding='utf-8')
data = []
for line in data_file:
    line = line.replace(":\", ", ":\"")

    line = line.replace(" True,", "\"True\",")
    line = line.replace(" True}", "\"True\"}")

    line = line.replace(" False,", "\"False\",")
    line = line.replace(" False}", "\"False\"}")

    line = line.replace(" None,", "\"None\",")
    line = line.replace(" None}", "\"None\"}")

    line = line.replace("\"{", "{")
    line = line.replace("}\"", "}")

    line = line.replace("\"u\'", "\"")
    line = line.replace("\'\"", "\"")

    line = line.replace(" \'", " \"")
    line = line.replace(",\'", ",\"")
    line = line.replace("{\'", "{\"")
    line = line.replace("\':", "\":")
    line = line.replace("\"\"", "\"")
    line = line.replace("\":\",", "\":\"\",")



    try:
        temp = json.loads(line)
        temp1 = recursively_clean_json(temp)
        data+=[temp1]
    except:
        pass

with open("./cleaned_data.txt", "w") as file:
    json.dump([ob for ob in data], file)
