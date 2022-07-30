from ast import Try
from package.haupteil.data_validation import DataValidation
from package.haupteil.model_trainer import ModelTrainer
from package.structure.structure import structure
from package.logger import logging
from package.exception import PackageException

from package.gebilde.ordner_gebilde import  DataIngestionOrdner, DataTransformOrdner, DataValidationOrdner, ModelTrainerOrdner
from package.gebilde.schmuck_gebilde import DataIngestionSchmuck
from package.haupteil.data_ingestion import DataIngestion
from package.haupteil.data_validation import DataValidation
from package.haupteil.data_transform import DataTransformation
from package.haupteil.data_validation import DataValidation


import os, sys


class Pipeline:

  def __init__(self,schmuck: structure= structure()) -> None:
      try:
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

  def start_model_trainer(self, data_transformation_ordner: DataTransformOrdner) -> ModelTrainerOrdner:
        try:
            model_trainer = ModelTrainer(model_trainer_ordner=self.schmuck.get_model_trainer_schmuck(),
                                         data_transformation_ordner=data_transformation_ordner
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise PackageException(e, sys) from e



  

  def run_pipeline(self):
        try:
            data_ingestion_ordner = self.start_data_ingestion()
            data_validation_ordner= self.start_data_validation(data_ingestion_ordner=data_ingestion_ordner)
            data_transformation_ordner = self.start_data_transformation(
                data_ingestion_ordner=data_ingestion_ordner,
                data_validation_ordner=data_validation_ordner
            )
            model_trainer_ordner = self.start_model_trainer(data_transformation_ordner=data_transformation_ordner)
        except Exception as e:
            raise PackageException(e, sys) from e  