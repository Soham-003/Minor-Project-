import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts", "ir_model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("Model training Initiated")
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model = XGBClassifier()
               
            

            model.fit(x_train,y_train)
            logging.info("Model Training Completed")
            y_test_pred = model.predict(x_test)
            logging.info("Model Prediction Completed")
            accuracy = accuracy_score(y_test,y_test_pred)
            logging.info(f"Model Accuracy: {accuracy}")
            cm = confusion_matrix(y_test,y_test_pred)
            logging.info(f"Confusion Matrix: \n{cm}")
            report = classification_report(y_test,y_test_pred)
            logging.info(f"Classification Report: \n{report}")

            save_object(
                file_path = self.model_trainer_config.model_path,
                obj = model
            )
            logging.info("Model Saved Successfully")

        except Exception as e:
            raise CustomException(e, sys)    
    