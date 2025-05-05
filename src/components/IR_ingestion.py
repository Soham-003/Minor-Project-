import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.IR_transformation import DataTransformation
from src.components.IR_model_trainer import ModelTrainer
from src.components.IR_transformation import DataTransformationConfig
from src.components.IR_model_trainer import ModelTrainerConfig



@dataclass
class DataIngestionConfig:
    train_path:str = os.path.join("artifacts","ir_train.csv")
    test_path:str = os.path.join("artifacts","ir_test.csv")
    raw_path:str = os.path.join("artifacts","ir_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_config(self):
       try:
           df = pd.read_csv('IR_notebooks/data/raw.csv')     
           logging.info("Data Ingestion Initiated")

           os.makedirs(os.path.dirname(self.ingestion_config.raw_path), exist_ok=True)

           df.to_csv(self.ingestion_config.raw_path, index=False,header = True)
           logging.info("Raw Data Ingested")
           train_set,test_set = train_test_split(df,test_size = 0.22,random_state = 42)
           logging.info("Data Split into Train and Test")
           train_set.to_csv(self.ingestion_config.train_path, index=False,header = True)
           test_set.to_csv(self.ingestion_config.test_path, index=False,header = True)
           logging.info("Data Ingestion Completed")

           return(
                 self.ingestion_config.train_path,
                 self.ingestion_config.test_path
            )
       except Exception as e:
              raise CustomException(e,sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_config()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)

    model_trainer = ModelTrainer()
    model_trainer.initiate_model_trainer(train_arr,test_arr)
