import pandas as pd

# Function to read the data file 
def read_data(file_path, **kwargs):
    raw_data = pd.read_json(file_path  ,**kwargs)
    return raw_data


# location to save and access model directory 
model_directory = "../models/current/Spacy_model/default/model_20230210-091453/"
client_id = 4

