import os,sys
from package.exception import PackageException
from package.logger import logging
from package.gebilde.schmuck_gebilde import DataValidationSchmuck
from package.gebilde.ordner_gebilde import DataIngestionOrdner,DataValidationOrdner
import pandas  as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json


class DataValidation:
    

    def __init__(self, data_validation_ordner:DataValidationSchmuck,
        data_ingestion_ordner:DataIngestionOrdner):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_validation_ordner = data_validation_ordner
            self.data_ingestion_ordner = data_ingestion_ordner
        except Exception as e:
            raise PackageException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_ordner.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_ordner.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise PackageException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_ordner.train_file_path
            test_file_path = self.data_ingestion_ordner.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_ordner.train_file_path
                testing_file = self.data_ingestion_ordner.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise PackageException(e,sys) from e

    
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            
            #Assigment validate training and testing dataset using schema file
            #1. Number of Column
            #2. Check the value of ocean proximity 
            # acceptable values     <1H OCEAN
            # INLAND
            # ISLAND
            # NEAR BAY
            # NEAR OCEAN
            #3. Check column names


            validation_status = True
            return validation_status 
        except Exception as e:
            raise PackageException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_ordner.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise PackageException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_ordner.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise PackageException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise PackageException(e,sys) from e

    def initiate_data_validation(self)-> DataValidationOrdner :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_ordner = DataValidationOrdner(
                schema_file_path=self.data_validation_ordner.schema_file_path,
                report_file_path=self.data_validation_ordner.report_file_path,
                report_page_file_path=self.data_validation_ordner.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation ordner: {data_validation_ordner}")
            return data_validation_ordner
        except Exception as e:
            raise PackageException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")
        


