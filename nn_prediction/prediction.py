import os
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Dense
from tensorflow import keras
from sklearn import preprocessing
import joblib
import matplotlib.pyplot as plt
from globals import *
import json

from nn_prediction.training.train import train_network


class NeuralNetworkPredictor:

    def __init__(self, model_name = MODEL_NAME):

        print("Initializing nn_predctor with model name {}".format(model_name))

        self.model_name = model_name
     
#load model
        model_path = 'nn_prediction/models/{}'.format(self.model_name)
        scaler_x_path = 'nn_prediction/models/{}/scaler_x.pkl'.format(self.model_name)
        scaler_y_path = 'nn_prediction/models/{}/scaler_y.pkl'.format(self.model_name)
        nn_settings_path = 'nn_prediction/models/{}/nn_settings.json'.format(self.model_name)

#chack if model is already trained
if not os.path.isdir(model_path):
            print("Model {} does not exist. Please train first".format(self.model_name))
            # train_network()

        self.model = keras.models.load_model(model_path)
        self.scaler_x = joblib.load(scaler_x_path) 
        self.scaler_y = joblib.load(scaler_y_path) 
        with open(nn_settings_path, 'r') as openfile:
            self.nn_settings = json.load(openfile)
    
        self.predict_delta = self.nn_settings['predict_delta']
        self.normalize_data = self.nn_settings['normalize_data']


    def predict_next_state(self, state, control_input):

    state_and_control = np.append(state, control_input)

        if(self.normalize_data):
    # Normalize input
            state_and_control_normalized = self.scaler_x.transform([state_and_control])
    # Predict
            predictions_normalized = self.model.predict(state_and_control_normalized)
    # Denormalize results
            prediction = self.scaler_y.inverse_transform(predictions_normalized)[0]

        else:
            prediction = self.model.predict([state_and_control.tolist()])

    
        if self.predict_delta:
        prediction = state + prediction

    return prediction






if __name__ == '__main__':

    next_state = predict_next_state([41.900000000000006,13.600000000000001,0.0,7.0,0.0,0.0,0.0], [0.06644491781040185,-0.40862345615368234])
    print("Next_state", next_state)
