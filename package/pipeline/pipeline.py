from ast import Try
from this import s
from package.haupteil.data_validation import DataValidation
from package.haupteil.model_trainer import ModelTrainer
from package.structure.structure import structure
from package.logger import logging
from package.exception import PackageException

from package.gebilde.ordner_gebilde import  DataIngestionOrdner, DataTransformOrdner, DataValidationOrdner, ModelTrainerOrdner,ModelEvaluationOrdner,ModelPusherOrdner
from package.gebilde.schmuck_gebilde import DataIngestionSchmuck,DataTransformationSchmuck,DataValidationSchmuck,ModelEvaluationSchmuck
from package.haupteil.data_ingestion import DataIngestion
from package.haupteil.data_validation import DataValidation
from package.haupteil.data_transform import DataTransformation
from package.haupteil.model_trainer import ModelTrainer
from package.haupteil.model_evaluation import ModelEvaluation
from package.haupteil.model_pusher import ModelPusher
from collections import namedtuple
from datetime import datetime
import pandas as pd
from package.bestandteil import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME
import os, sys
import uuid


Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "ordner_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path", "accuracy", "is_model_accepted"])


class Pipeline:

     experiment: Experiment = Experiment(*([None] * 11))
     experiment_file_path = None

     def __init__(self,schmuck: structure= structure()) -> None:


        try:
            os.makedirs(schmuck.training_pipeline_ordner.ordner_dir, exist_ok=True)
            Pipeline.experiment_file_path=os.path.join(schmuck.training_pipeline_ordner.ordner_dir,EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME)
            #super().__init__(daemon=False, name="pipeline")

            self.schmuck=schmuck
        except Exception as e:
            raise PackageException(e, sys) from e


     def start_data_ingestion(self) -> DataIngestionOrdner:
        try:
            data_ingestion = DataIngestion(data_ingestion_ordner=self.schmuck.get_data_ingestion_schmuck())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise PackageException(e, sys) from e
   
     def start_data_validation(self,data_ingestion_ordner:DataIngestionOrdner)\
         -> DataValidationOrdner:
         try:
            data_validation=DataValidation(data_validation_ordner=self.schmuck.get_data_validation_schmuck(),
                                            data_ingestion_ordner=data_ingestion_ordner       
                                              )
            return data_validation.initiate_data_validation()
    
         except Exception as e :
            raise PackageException(e,sys) from e
  
     def start_data_transformation(self,
                                  data_ingestion_ordner: DataIngestionOrdner,
                                  data_validation_ordner: DataValidationOrdner
                                  ) -> DataTransformOrdner:
        try:
            data_transformation = DataTransformation(
                data_transformation_ordner=self.schmuck.get_data_transformation_schmuck(),
                data_ingestion_ordner=data_ingestion_ordner,
                data_validation_ordner=data_validation_ordner
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise PackageException(e, sys)

     def start_model_trainer(self, data_transformation_ordner: DataTransformOrdner,data_ingestion_ordner:DataIngestionOrdner) -> ModelTrainerOrdner:
        try:
            model_trainer = ModelTrainer(model_trainer_ordner=self.schmuck.get_model_trainer_schmuck(),
                                         data_transformation_ordner=data_transformation_ordner,
                                         data_ingestion_ordner=data_ingestion_ordner)
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise PackageException(e, sys) from e

     def start_model_evaluation(self, data_ingestion_ordner: DataIngestionOrdner,
                               data_validation_ordner: DataValidationOrdner,
                               model_trainer_ordner: ModelTrainerOrdner) -> ModelEvaluationOrdner:
        try:
            model_eval = ModelEvaluation(
                model_evaluation_ordner=self.schmuck.get_model_evaluation_schmuck(),
                data_ingestion_ordner=data_ingestion_ordner,
                data_validation_ordner=data_validation_ordner,
                model_trainer_ordner=model_trainer_ordner)
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise PackageException(e, sys) from e

    
     def start_model_pusher(self, model_eval_ordner: ModelEvaluationOrdner) -> ModelPusherOrdner:
        try:
            model_pusher = ModelPusher(
                model_pusher_ordner=self.schmuck.get_model_pusher_schmuck(),
                model_evaluation_ordner=model_eval_ordner
            )
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise PackageException(e, sys) from e


  

     def run_pipeline(self):
        try:
            if Pipeline.experiment.running_status:
                logging.info("Pipeline is already running")
                return Pipeline.experiment
            # data ingestion
            logging.info("Pipeline starting.")

            experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(experiment_id=experiment_id,
                                             initialization_timestamp=self.schmuck.time_stamp,
                                             ordner_time_stamp=self.schmuck.time_stamp,
                                             running_status=True,
                                             start_time=datetime.now(),
                                             stop_time=None,
                                             execution_time=None,
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             is_model_accepted=None,
                                             message="Pipeline has been started.",
                                             accuracy=None,
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")

            self.save_experiment()

            data_ingestion_ordner = self.start_data_ingestion()
            data_validation_ordner= self.start_data_validation(data_ingestion_ordner=data_ingestion_ordner)
            data_transformation_ordner = self.start_data_transformation(
                data_ingestion_ordner=data_ingestion_ordner,
                data_validation_ordner=data_validation_ordner
            )
            
            model_trainer_ordner = self.start_model_trainer( data_ingestion_ordner=data_ingestion_ordner, data_transformation_ordner =  data_transformation_ordner)
            model_evaluation_ordner = self.start_model_evaluation(data_ingestion_ordner=data_ingestion_ordner,
                                                                    data_validation_ordner=data_validation_ordner,
                                                                    model_trainer_ordner=model_trainer_ordner)

            if model_evaluation_ordner.is_model_accepted:
                model_pusher_ordner = self.start_model_pusher(model_evaluation_ordner=model_evaluation_ordner)
                logging.info(f'Model pusher artifact: {model_pusher_ordner}')
            else:
                logging.info("Trained model rejected.")
            logging.info("Pipeline completed.")

      

            
            stop_time = datetime.now()
            Pipeline.experiment = Experiment(experiment_id=Pipeline.experiment.experiment_id,
                                             initialization_timestamp=self.schmuck.time_stamp,
                                             artifact_time_stamp=self.schmuck.time_stamp,
                                             running_status=False,
                                             start_time=Pipeline.experiment.start_time,
                                             stop_time=stop_time,
                                             execution_time=stop_time - Pipeline.experiment.start_time,
                                             message="Pipeline has been completed.",
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             is_model_accepted=model_evaluation_ordner.is_model_accepted,
                                             accuracy=model_trainer_ordner.model_accuracy
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()
        except Exception as e:
            raise PackageException(e, sys) from e

     def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e

     def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key: [value] for key, value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp": [datetime.now()],
                    "experiment_file_path": [os.path.basename(Pipeline.experiment.experiment_file_path)]})

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok=True)
                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index=False, header=False, mode="a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, mode="w", index=False, header=True)
            else:
                print("First start experiment")
        except Exception as e:
            raise PackageException(e, sys) from e

     @classmethod
     def get_experiments_status(cls, limit: int = 5) -> pd.DataFrame:

        try:
            if os.path.exists(Pipeline.experiment_file_path):
                df = pd.read_csv(Pipeline.experiment_file_path)
                limit = -1 * int(limit)
                return df[limit:].drop(columns=["experiment_file_path", "initialization_timestamp"], axis=1)
            else:
                return pd.DataFrame()
        except Exception as e:
            raise PackageException(e, sys) from e