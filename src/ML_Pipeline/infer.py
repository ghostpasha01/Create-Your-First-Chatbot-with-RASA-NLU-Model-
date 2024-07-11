from ML_Pipeline.utlis import model_directory
from rasa_nlu.model import Metadata, Interpreter
import spacy


# specify language as "en" for spacy pipeline
nlp = spacy.load("en_core_web_sm")

# load model directory in memory by interpreter
interpreter = Interpreter.load(model_directory)


def infer_message(message):
    """
    :param message: message to be processed by model ,to predict intent and entities
    :return: returns intents and entities by model to be predicted by model
    """
    response = interpreter.parse(message)
    return response
