from package.logger import logging
from package.exception import PackageException
from package.gebilde.ordner_gebilde import ModelPusherOrdner, ModelEvaluationOrdner
from package.gebilde.schmuck_gebilde import ModelPusherSchmuck
import os, sys
import shutil


class ModelPusher:

    def __init__(self, model_pusher_ordner: ModelPusherSchmuck,
                 model_evaluation_ordner: ModelEvaluationOrdner
                 ):
        try:
            logging.info(f"{'>>' * 30}Model Pusher log started.{'<<' * 30} ")
            self.model_pusher_ordner = model_pusher_ordner
            self.model_evaluation_ordner = model_evaluation_ordner

        except Exception as e:
            raise PackageException(e, sys) from e

    def export_model(self) -> ModelPusherOrdner:
        try:
            evaluated_model_file_path = self.model_evaluation_ordner.evaluated_model_path
            export_dir = self.model_pusher_ordner.export_dir_path
            model_file_name = os.path.basename(evaluated_model_file_path)
            export_model_file_path = os.path.join(export_dir, model_file_name)
            logging.info(f"Exporting model file: [{export_model_file_path}]")
            os.makedirs(export_dir, exist_ok=True)

            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)
            #we can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket
            logging.info(
                f"Trained model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")

            model_pusher_ordner = ModelPusherOrdner(is_model_pusher=True,
                                                        export_model_file_path=export_model_file_path
                                                        )
            logging.info(f"Model pusher artifact: [{model_pusher_ordner}]")
            return model_pusher_ordner
        except Exception as e:
            raise PackageException(e, sys) from e

    def initiate_model_pusher(self) -> ModelPusherOrdner:
        try:
            return self.export_model()
        except Exception as e:
            raise PackageException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")
