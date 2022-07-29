from cgi import test
from sklearn import preprocessing
from package.exception import PackageException
from package.logger import logging
from package.gebilde.schmuck_gebilde import DataTransformationSchmuck
from package.gebilde.ordner_gebilde import DataIngestionOrdner,\
DataValidationOrdner,DataTransformOrdner
import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from package.bestandteil import *
from package.util.util import read_yaml_file, save_object,save_numpy_array_data,load_data








class DataTransformation:

    def __init__(self, data_transformation_ordner: DataTransformationSchmuck,
                 data_ingestion_ordner: DataIngestionOrdner,
                 data_validation_ordner: DataValidationOrdner
                 ):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_ordner= data_transformation_ordner
            self.data_ingestion_ordner = data_ingestion_ordner
            self.data_validation_ordner = data_validation_ordner

        except Exception as e:
            raise PackageException(e,sys) from e

    

    def get_data_transformer_object(self)->ColumnTransformer:


        try:

            schema_file_path = self.data_validation_ordner.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]


            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy="median")),
                 ('scaler', StandardScaler())]
            )

            cat_pipeline = Pipeline(steps=[
                 ('impute', SimpleImputer(strategy="most_frequent")),
                 ('one_hot_encoder', OneHotEncoder()),
                 ('scaler', StandardScaler(with_mean=False))
            ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")


            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])

            return preprocessing

          
        except Exception as e:
            raise PackageException(e,sys) from e   


    def initiate_data_transformation(self)->DataTransformOrdner:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()


            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_ordner.train_file_path
            test_file_path = self.data_ingestion_ordner.test_file_path
            

            schema_file_path = self.data_validation_ordner.schema_file_path
            
            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]


            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
            

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            #input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            #input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            #train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]

            #test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_ordner.transformed_train_dir
            transformed_test_dir = self.data_transformation_ordner.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")
            
            #save_numpy_array_data(file_path=transformed_train_file_path),#array=train_arr)
            #save_numpy_array_data(file_path=transformed_test_file_path),#array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_ordner.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_ordner = DataTransformOrdner(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preprocessing_obj_file_path

            )
            logging.info(f"Data transformationa ordner: {data_transformation_ordner}")
            return data_transformation_ordner
        except Exception as e:
            raise PackageException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")