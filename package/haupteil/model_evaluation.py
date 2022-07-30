from package.logger import logging
from package.exception import PackageException
from package.gebilde.schmuck_gebilde import ModelEvaluationSchmuck
from package.gebilde.ordner_gebilde import DataIngestionOrdner,DataValidationOrdner,ModelTrainerOrdner,ModelEvaluationOrdner
from package.bestandteil import *
import numpy as np
import os
import sys
from package.util.util import write_yaml_file, read_yaml_file, load_object,load_data
from package.gebilde.model_factory import evaluate_classification_model




class ModelEvaluation:

    def __init__(self, model_evaluation_ordner: ModelEvaluationSchmuck,
                 data_ingestion_ordner: DataIngestionOrdner,
                 data_validation_ordner: DataValidationOrdner,
                 model_trainer_ordner: ModelTrainerOrdner):
        try:
            logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.model_evaluation_ordner = model_evaluation_ordner
            self.model_trainer_ordner = model_trainer_ordner
            self.data_ingestion_ordner = data_ingestion_ordner
            self.data_validation_ordner = data_validation_ordner
        except Exception as e:
            raise PackageException(e, sys) from e

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_ordner.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path,
                                )
                return model
            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model

            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise PackageException(e, sys) from e

    def update_evaluation_report(self, model_evaluation_ordner: ModelEvaluationOrdner):
        try:
            eval_file_path = self.model_evaluation_ordner.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous eval result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_ordner.evaluated_model_path,
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_ordner.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_content}")
            write_yaml_file(file_path=eval_file_path, data=model_eval_content)

        except Exception as e:
            raise PackageException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationOrdner:
        try:
            trained_model_file_path = self.model_trainer_ordner.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_ordner.train_file_path
            test_file_path = self.data_ingestion_ordner.test_file_path

            schema_file_path = self.data_validation_ordner.schema_file_path

            train_dataframe = load_data(file_path=train_file_path,
                                                           schema_file_path=schema_file_path,
                                                           )
            test_dataframe = load_data(file_path=test_file_path,
                                                          schema_file_path=schema_file_path,
                                                          )
            schema_content = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema_content[TARGET_COLUMN_KEY]

            # target_column
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")

            # dropping target column from the dataframe
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")

            model = self.get_best_model()

            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model")
                model_evaluation_ordner = ModelEvaluationOrdner(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_ordner)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_ordner} created")
                return model_evaluation_ordner

            model_list = [model, trained_model_object]

            metric_info_ordner = evaluate_classification_model(model_list=model_list,
                                                               X_train=train_dataframe,
                                                               y_train=train_target_arr,
                                                               X_test=test_dataframe,
                                                               y_test=test_target_arr,
                                                               base_accuracy=self.model_trainer_ordner.model_accuracy,
                                                               )
            logging.info(f"Model evaluation completed. model metric ordner: {metric_info_ordner}")

            if metric_info_ordner is None:
                response = ModelEvaluationOrdner(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path
                                                   )
                logging.info(response)
                return response

            if metric_info_ordner.index_number == 1:
                model_evaluation_artifact = ModelEvaluationOrdner(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_ordner)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_ordner} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_ordner = ModelEvaluationOrdner(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_ordner
        except Exception as e:
            raise PackageException(e, sys) from e

    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")