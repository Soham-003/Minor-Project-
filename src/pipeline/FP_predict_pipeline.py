import sys 
import os
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def predict(self,features):
        try:
            preprocessor_path = os.path.join("artifacts","fp_preprocessor.pkl")
            model_path = os.path.join("artifacts","fp_model.pkl")
            print("Before Loading")
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            print("After Loading")
            data_scaled = preprocessor.transform(features)
            print("After Transforming")
            pred = model.predict(data_scaled)
            print("After Predicting")
            return pred[0]
        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(
            self,
            N:int,
            P:int,
            K:int,
            temperature:int,
            humidity:int,
            moisture:int,
            soil_type:str,
            crop:str,
    ):
        self.N = N
        self.P = P
        self.K = K
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture
        self.soil_type = soil_type
        self.crop = crop 

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Nitrogen': [self.N],
                'Phosphorous': [self.P],
                'Potassium': [self.K],
                'Temparature': [self.temperature],
                'Humidity ': [self.humidity],
                'Moisture': [self.moisture],
                'Soil Type': [self.soil_type],
                'Crop Type': [self.crop]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)       