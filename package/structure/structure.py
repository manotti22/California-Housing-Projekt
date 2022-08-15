from package.gebilde.schmuck_gebilde import DataIngestionSchmuck, DataValidationSchmuck, ModelEvaluationSchmuck, ModelPusherSchmuck, ModelTrainerSchmuck, TrainingPipelineSchmuck,DataTransformationSchmuck  
from package.util.util import read_yaml_file
from package.logger import logging
import sys,os
from package.bestandteil import *
from package.exception import PackageException


class structure:

    def __init__(self,
        schmuck_file_path:str =SCHMUCK_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP
        ) -> None:
        try:
            self.schmuck_info  = read_yaml_file(file_path=schmuck_file_path)
            self.training_pipeline_ordner= self.get_training_pipeline_schmuck()
            self.time_stamp= current_time_stamp


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
            data_ingestion_info = self.schmuck_info[DATA_INGESTION_ORDNER_KEY]
            
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

    def get_data_validation_schmuck(self) -> DataValidationSchmuck:
        try:
            ordner_dir = self.training_pipeline_ordner.ordner_dir

            data_validation_ordner_dir=os.path.join(
                ordner_dir,
                DATA_VALIDATION_ORDNER_DIR_NAME,
                self.time_stamp
            )
            data_validation_ordner = self.schmuck_info[DATA_VALIDATION_ORDNER_KEY]


            schema_file_path = os.path.join(ROOT_DIR,
            data_validation_ordner[DATA_VALIDATION_SCHEMA_DIR_KEY],
            data_validation_ordner[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path = os.path.join(data_validation_ordner_dir,
            data_validation_ordner[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(data_validation_ordner_dir,
            data_validation_ordner[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]

            )

            data_validation_ordner = DataValidationSchmuck(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
            )
            return data_validation_ordner
        except Exception as e:
            raise PackageException(e,sys) from e
    
    def get_data_transformation_schmuck(self) -> DataTransformationSchmuck:
        try:
            ordner_dir = self.training_pipeline_ordner.ordner_dir

            data_transformation_ordner_dir=os.path.join(
                ordner_dir,
                DATA_TRANSFORM_ORDNER_DIR,
                self.time_stamp
            )

            data_transformation_schmuck_info=self.schmuck_info[DATA_TRANSFORM_ORDNER_KEY]


            preprocessed_object_file_path = os.path.join(
                data_transformation_ordner_dir,
                data_transformation_schmuck_info[DATA_TRANSFORM_PREPROCESSING_DIR_KEY],
                data_transformation_schmuck_info[DATA_TRANSFORM_PREPROCESSED_FILE_NAME_KEY]
            )

            
            transformed_train_dir=os.path.join(
            data_transformation_ordner_dir,
            data_transformation_schmuck_info[DATA_TRANSFORM_DIR_NAME_KEY],
            data_transformation_schmuck_info[DATA_TRANSFORM_TRAIN_DIR_NAME_KEY]
            )


            transformed_test_dir = os.path.join(
            data_transformation_ordner_dir,
            data_transformation_schmuck_info[DATA_TRANSFORM_DIR_NAME_KEY],
            data_transformation_schmuck_info[DATA_TRANSFORM_TEST_DIR_NAME_KEY]

            )
            

            data_transformation_ordner=DataTransformationSchmuck(
                preprocessed_object_file_path=preprocessed_object_file_path,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir
            )

            logging.info(f"Data transformation config: {data_transformation_ordner}")
            return data_transformation_ordner
        except Exception as e:
            raise PackageException(e,sys) from e

    
    def get_model_trainer_schmuck(self) -> ModelTrainerSchmuck:
        try:
            ordner_dir = self.training_pipeline_ordner.ordner_dir

            model_trainer_ordner_dir=os.path.join(
                ordner_dir,
                MODEL_TRAINER_ORDNER_DIR,
                self.time_stamp
            )
            model_trainer_schmuck_info = self.schmuck_info[MODEL_TRAINER_ORDNER_KEY]
            trained_model_file_path = os.path.join(model_trainer_ordner_dir,
            model_trainer_schmuck_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_schmuck_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
            )
            model_ordner_file_path = os.path.join(model_trainer_ordner_dir,
            model_trainer_schmuck_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_schmuck_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
            )

            model_ordner_dir = r'C:\Users\HPr\Desktop\Projekte\Travel_Package_Project\package\ordner\model_trainer\2022-08-03-14-54-03\trained_model'
            os.makedirs(model_ordner_dir,exist_ok=True)
            model_ordner_file_path=os.path.basename(model_ordner_dir)
            model_ordner_file_path = os.path.join(model_ordner_dir,model_ordner_file_path)


            
            
            base_accuracy = model_trainer_schmuck_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_ordner = ModelTrainerSchmuck(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_ordner_file_path= model_ordner_file_path
                )
            
            logging.info(f"Model trainer ordner: {model_trainer_ordner}")
            return model_trainer_ordner
        except Exception as e:
            raise PackageException(e,sys) from e
    

    def get_model_evaluation_schmuck(self) ->ModelEvaluationSchmuck:
        try:
            model_evaluation_ordner = self.schmuck_info[MODEL_EVALUATION_ORDNER_KEY]
            ordner_dir = os.path.join(self.training_pipeline_ordner.ordner_dir,
                                        MODEL_EVALUATION_ORDNER_DIR, )

            model_evaluation_file_path = os.path.join(ordner_dir,
                                                    model_evaluation_ordner[MODEL_EVALUATION_FILE_NAME_KEY])
            response = ModelEvaluationSchmuck(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Ordner: {response}.")
            return response
        except Exception as e:
            raise PackageException(e,sys) from e
    
    def get_model_pusher_schmuck(self) -> ModelPusherSchmuck:
        try:
            time_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            model_pusher_schmuck_info = self.schmuck_info[MODEL_PUSHER_ORDNER_KEY]
            export_dir_path = os.path.join(ROOT_DIR, model_pusher_schmuck_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY],
                                           time_stamp)

            model_pusher_ordner = ModelPusherSchmuck(export_dir_path=export_dir_path)
            logging.info(f"Model pusher ordner {model_pusher_ordner}")
            return model_pusher_ordner

        except Exception as e:
            raise PackageException(e,sys) from e
    

    def get_training_pipeline_schmuck(self) ->TrainingPipelineSchmuck:
            try:
                training_pipeline_ordner = self.schmuck_info[TRAINING_PIPELINE_ORDNER_KEY]
                ordner_dir = os.path.join(ROOT_DIR,
                training_pipeline_ordner[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_ordner[TRAINING_PIPELINE_ORDNER_DIR_KEY]
                )

                training_pipeline_ordner = TrainingPipelineSchmuck(ordner_dir=ordner_dir)
                logging.info(f"Training pipleine Schmuck: {training_pipeline_ordner}")
                return training_pipeline_ordner
            except Exception as e:
                raise PackageException(e,sys) from e