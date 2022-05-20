import json
import pandas as pd

with open('data.txt') as json_file:
    data = json.load(json_file)
dataframe = pd.DataFrame(data)
    #dataframe = dataframe.append(pd.read_json(data))
#for item in data:
 #   print(type(item))
  #  print(item)

#dataframe = pd.read_json(data)
print(type(dataframe))
print(dataframe)

print(dataframe.equipment.unique())
print(len(dataframe.equipment.unique()))