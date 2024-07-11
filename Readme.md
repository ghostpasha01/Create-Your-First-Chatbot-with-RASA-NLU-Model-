# Create Your First Chatbot with RASA NLU Model and Python

This project aims to build a conversational agent for an e-commerce website using the Rasa framework. The chatbot will be able to understand and respond to various user inquiries related to products and orders.

## Intent Classification

The chatbot will be trained to identify and categorize user inquiries into the following intents:

1. `product_info`: This intent is used when the user wants to get information about a product. It depends on the entities `product` and `location`.

2. `ask_price`: This intent is used when the user wants to know the price of a product. It depends on the entities `product` and `location`.

3. `cancel_order`: This intent is used when the user wants to cancel an existing order. It depends on the entity `order_id`.

## Data Preparation

The data used to train the chatbot will be in the form of example user inquiries and the corresponding intents and entities. This data will be stored in a file in the JSON or YAML format and will be used to train the Rasa NLU model.

## Model Training

The Rasa NLU model will be trained using the Rasa library and the training data. The model configuration, such as the pipeline and hyperparameters, will be specified in a separate configuration file. The trained model will be saved to a directory for use in the chatbot application.

## Execution Instructions
The following steps can be followed to execute the project with python 3.6.4:

1. Create and activate a virtual environment with python3.6.4

2. Install the required packages with the requirements.txt file in src directory.
   `pip install -r requirements.txt`

3. Download spaCy's language model:
   `python -m spacy download en_core_web_sm`

4. Run the rasa_chatbot.ipynb in the lib folder using Jupyter Notebook.

5. Run the engine script:
   `python Engine.py`




