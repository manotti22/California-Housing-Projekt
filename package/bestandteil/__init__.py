
import os
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    
ROOT_DIR = os.getcwd()  #to get current working directory
SCHMUCK_DIR = "schmuck"
SCHMUCK_FILE_NAME = "schmuck.yaml"
SCHMUCK_FILE_PATH = os.path.join(ROOT_DIR,SCHMUCK_DIR,SCHMUCK_FILE_NAME)



CURRENT_TIME_STAMP = get_current_time_stamp()




# Training pipeline related variable
TRAINING_PIPELINE_ORDNER_KEY = "training_pipeline_ordner"
TRAINING_PIPELINE_ORDNER_DIR_KEY = "ordner_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


# Data Ingestion related variable

DATA_INGESTION_ORDNER_KEY = "data_ingestion_ordner"
DATA_INGESTION_ORDNER_DIR = "data_ingestion"
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = "tgz_download_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"

# Data Validation related variable

# Data Validation related variables
DATA_VALIDATION_ORDNER_KEY = "data_validation_ordner"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_ORDNER_DIR_NAME="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"



# Data Transformation related variables
DATA_TRANSFORM_ORDNER_DIR = "data_transform"
DATA_TRANSFORM_ORDNER_KEY = "data_transform_ordner"
DATA_TRANSFORM_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORM_TRAIN_DIR_NAME_KEY = "transformed_train_dir"
DATA_TRANSFORM_TEST_DIR_NAME_KEY = "transformed_test_dir"
DATA_TRANSFORM_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORM_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"



COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"

NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"


TARGET_COLUMN_KEY="target_column"


# Model Training related variables

MODEL_TRAINER_ORDNER_DIR = "model_trainer"
MODEL_TRAINER_ORDNER_KEY = "model_trainer_ordner"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_ORDNER_DIR_KEY = "model_ordner_dir"
MODEL_TRAINER_MODEL_ORDNER_FILE_NAME_KEY = "model_ordner_file_name"


MODEL_EVALUATION_ORDNER_KEY = "model_evaluation_ordner"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ORDNER_DIR = "model_evaluation"
# Model Pusher config key
MODEL_PUSHER_ORDNER_KEY = "model_pusher_ordner"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = "model_export_dir"

BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"