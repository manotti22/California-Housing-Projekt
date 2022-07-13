from collections import namedtuple



DataIngestionOrdner = namedtuple("DataIngestionOrdner",
[ "train_file_path", "test_file_path", "is_ingested", "message"])


DataValidationOrdner = namedtuple("DataValidationOrdner",
["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])


DataTransformOrdner = namedtuple("DataTransformOrdner",
 ["is_transformed", "message", "transformed_train_file_path","transformed_test_file_path",
     "preprocessed_object_file_path"])

ModelTrainerOrdner = namedtuple("ModelTrainerOrdner", ["is_trained", "message", "trained_model_file_path",
                                                           "train_rmse", "test_rmse", "train_accuracy", "test_accuracy",
                                                           "model_accuracy"])

ModelEvaluationOrdner = namedtuple("ModelEvaluationOrdner", ["is_model_accepted", "evaluated_model_path"])

ModelPusherOrdner = namedtuple("ModelPusherOrdner", ["is_model_pusher", "export_model_file_path"])