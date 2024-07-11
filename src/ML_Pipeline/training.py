import spacy
import os
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.training_data import load_data

nlp = spacy.load("en_core_web_sm")


def select_examples(initial_data, nb_of_examples):
    """
    :param initial_data: rasa nlu data
    :param nb_of_examples: no of examples as a threshold on how do we need to split the data
    :return:training and testing dataframe after splitting the initial data
    """
    if nb_of_examples > len(initial_data["rasa_nlu_data"]["common_examples"]):
        nb_of_examples = len(initial_data["rasa_nlu_data"]["common_examples"])
    training_examples_list = []
    test_examples_list = []
    training_df = initial_data.copy()
    test_df = initial_data.copy()

    examples_df = pd.DataFrame.from_records(initial_data["rasa_nlu_data"]["common_examples"])
    serie_distOfExamples = examples_df["intent"].value_counts() / len(examples_df)
    for intent in serie_distOfExamples.index.values:
        n = int(serie_distOfExamples[intent] * nb_of_examples)
        l = examples_df[examples_df["intent"] == intent].index.values
        examples_samp = random.sample(list(l), n)
        training_examples_ids = random.sample(examples_samp, int(n * 0.8))
        for ex_id in training_examples_ids:
            examples_samp.remove(ex_id)
        for index_train in training_examples_ids:
            training_examples_list.append(initial_data["rasa_nlu_data"]["common_examples"][index_train])
        for index_test in examples_samp:
            test_examples_list.append(initial_data["rasa_nlu_data"]["common_examples"][index_test])

    training_df["rasa_nlu_data"]["common_examples"] = training_examples_list
    test_df["rasa_nlu_data"]["common_examples"] = test_examples_list

    return training_df, test_df


def construct_jsonExampleFile(training_df, test_df, initial_data):
    """
    :param training_df: training dataframe
    :param test_df: testing dataframe
    :return: None, writes both the dataframe into specified path
    """
    training_df.to_json('../data/training_data.json')
    test_df.to_json('../data/test_data.json')


def examplesDist_plot(log_pd):
    """
    :param log_pd: data as the rasa nlu data,
    :return: None, calculate value count per intent and plots that using matplotlib
    """
    percent = pd.DataFrame.from_records(log_pd["rasa_nlu_data"]["common_examples"])["intent"].value_counts()
    percent.plot(kind='bar', figsize=(10, 8))
    plt.ylabel("Number of examples per intent")
    plt.xlabel("Intents")
    plt.title("Number of examples per intent")
    plt.show()


def trainModel(pipeline, model_dir):
    """
    :param pipeline: pipleine path to be loaded as the config in the Trainer
    :param model_dir: model dir where we need to store the model ,after training model using Trainer
    :return: model_dir where the trained model has been trained and saved.
    """
    path_to_data = "../data/training_data.json"
    training_data = load_data(path_to_data)
    trainer = Trainer(config.load(pipeline))
    path_to_model = "../output/" + model_dir
    model_directory = trainer.persist(path_to_model)
    return model_directory


def train_rasa():
    """
    :return: read json,select files,split those into training ,testin,start training and writes that in storage specified
    """
    data = "../data/data.json"
    initial_data = pd.read_json(data)

    train, test = select_examples(initial_data, 1000)
    construct_jsonExampleFile(train, test, initial_data)

    start = time.time()
    model_dir = trainModel("../data/spacy_config.yml", "Spacy_model")
    end = time.time()
    print("The training took ", (end - start) / 60, " mins for execution")
    print("Model has been saved here:", model_dir)
