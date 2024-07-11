from ML_Pipeline.utlis import read_data
from ML_Pipeline.training import train_rasa
from ML_Pipeline.infer import infer_message
from ML_Pipeline.dialog import process_message
from ML_Pipeline.utlis import client_id
import uuid


## read the json file 
initial_data = read_data("../data/data.json")



### train rasa with the specified data inside Input Folder
train_rasa()
print("read succesfully")


### infer rasa intent and entity on one single message using infer_message
message = "Can you tell me about television"
response = infer_message(message)
print(response)



### dialog conversation and context management
if __name__ == "__main__":
    chat_id = uuid.uuid4()
    while True:
        message = input(">>")
        response = process_message(message, client_id, chat_id)
print("done")
