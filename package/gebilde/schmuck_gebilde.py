from collections import namedtuple


DataIngestionSchmuck=namedtuple("DataIngestionSchmuck",
["dataset_download_url","tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])


DataValidationSchmuck = namedtuple("DataValidationSchmuck", ["schema_file_path","report_file_path","report_page_file_path"])

DataTransformationSchmuck = namedtuple("DataTransformationSchmuck", ["transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessed_object_file_path"])


ModelTrainerSchmuck = namedtuple("ModelTrainerSchmuck", ["trained_model_file_path","base_accuracy","model_ordner_file_path"])

ModelEvaluationSchmuck = namedtuple("ModelEvaluationSchmuck", ["model_evaluation_file_path","time_stamp"])


ModelPusherSchmuck = namedtuple("ModelPusherSchmuck", ["export_dir_path"])

TrainingPipelineSchmuck = namedtuple("TrainingPipelineSchmuck", ["ordner_dir"])