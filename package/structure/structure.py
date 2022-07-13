
from package.gebilde.schmuck_gebilde import DataIngestionSchmuck, DataTransformationSchmuck,DataValidationSchmuck,   \
ModelTrainerSchmuck,ModelEvaluationSchmuck,ModelPusherSchmuck,TrainingPipelineSchmuck
from package.util.util import read_yaml_file
from package.logger import logging
import sys,os
from package.bestandteil import *
from package.exception import PackageException


class Structure:

    def __init__(self,
        schmuck_file_path:str =SCHMUCK_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP
        ) -> None:
        try:
            self.schmuck_info  = read_yaml_file(file_path=schmuck_file_path)
            self.training_pipeline_ordner = self.get_training_pipeline_schmuck()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise PackageException(e,sys) from e


    def get_data_ingestion_schmuck(self) ->DataIngestionSchmuck:
        try:
            ordner_dir = self.training_pipeline_ordner.ordner_dir
            data_ingestion_ordner_dir=os.path.join(
                ordner_dir,
                DATA_INGESTION_ORDNER_DIR,
                self.time_stamp
            )
            data_ingestion_info = self.ordner_info[DATA_INGESTION_ORDNER_KEY]
            
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            tgz_download_dir = os.path.join(
                data_ingestion_ordner_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            raw_data_dir = os.path.join(data_ingestion_ordner_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                data_ingestion_ordner_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir =os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )


            data_ingestion_ordner=DataIngestionSchmuck(
                dataset_download_url=dataset_download_url, 
                tgz_download_dir=tgz_download_dir, 
                raw_data_dir=raw_data_dir, 
                ingested_train_dir=ingested_train_dir, 
                ingested_test_dir=ingested_test_dir
            )
            logging.info(f"Data Ingestion ORDNER: {data_ingestion_ordner}")
            return data_ingestion_ordner
        except Exception as e:
            raise PackageException(e,sys) from e

def get_training_pipeline_schmuck(self) ->TrainingPipelineSchmuck:
        try:
            training_pipeline_ordner = self.config_info[TRAINING_PIPELINE_ORDNER_KEY]
            ordner_dir = os.path.join(ROOT_DIR,
            training_pipeline_ordner[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_ordner[TRAINING_PIPELINE_ORDNER_DIR_KEY]
            )

            training_pipeline_ordner = TrainingPipelineSchmuck(ordner_dir=ordner_dir)
            logging.info(f"Training pipleine Schmuck: {training_pipeline_ordner}")
            return training_pipeline_ordner
        except Exception as e:
            raise PackageException(e,sys) from e