import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join("artifacts","fp_preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            num_features = ['Nitrogen', 'Potassium', 'Phosphorous', 'Temparature', 'Humidity ', 'Moisture']
            cat_festures = ['Crop Type','Soil Type']

            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean = False))
                ]
            )
            logging.info('Numerical and Categorical pipelines are created')
            preprocessor = ColumnTransformer(
                [
                    ('numerical',num_pipeline,num_features),
                    ('categorical',cat_pipeline,cat_festures)
                ]
            
            )
            logging.info('Preprocessor is created')
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Data Transformation Initiated')

            preprocessing_obj = self.get_data_transformation_object()
            target_column = 'Fertilizer Name'

            input_feature_train_df = train_df.drop(columns=[target_column],axis = 1)
            train_df[target_column] = train_df[target_column].map(
                {
                    'Urea': 6,
                    'DAP': 3,
                    '14-35-14': 2,
                    '28-28': 1,
                    '17-17-17': 4,
                    '20-20': 5,
                    '10-26-26': 0,
                }
            )
            test_df[target_column] = test_df[target_column].map(
                {
                    'Urea': 6,
                    'DAP': 3,
                    '14-35-14': 2,
                    '28-28': 1,
                    '17-17-17': 4,
                    '20-20': 5,
                    '10-26-26': 0,
                }
            )
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column],axis = 1)
            target_feature_test_df = test_df[target_column]
            logging.info('Input and Target features are separated')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            logging.info('Input features are transformed')

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info('Train and Test arrays are created')

            logging.info('Preprocessor is saved')

            save_object(
                file_path = self.data_transformation_config.preprocessor_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
            



