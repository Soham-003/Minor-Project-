import sys 
import os
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object

class IR_PredictPipeline:
    def predict(self,features):
        try:
            preprocessor_path = os.path.join("artifacts","ir_preprocessor.pkl")
            model_path = os.path.join("artifacts","ir_model.pkl")
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
        
class IR_CustomData:
    def __init__(
            self,
            Soil_Moisture:int,
            Temperature:int,
            Soil_Humidity:int,
            Air_Humidity:int,
            Pressure:int,
            
    ):
        self.Soil_Moisture= Soil_Moisture
        self.Temperature= Temperature
        self.Soil_Humidity= Soil_Humidity
        self.Air_Humidity= Air_Humidity
        self.Pressure= Pressure
        

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "Soil Moisture": [self.Soil_Moisture],
                "Temperature": [self.Temperature],
                "Soil Humidity": [self.Soil_Humidity],
                "Air Humidity": [self.Air_Humidity],
                "Pressure": [self.Pressure],
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)       