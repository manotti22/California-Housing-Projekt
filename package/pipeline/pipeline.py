from ast import Try
from package.structure.structure import Structure
from package.logger import logging, get_log_file_name
from package.exception import PackageException

from package.gebilde.ordner_gebilde import  DataIngestionOrdner
from package.gebilde.schmuck_gebilde import DataIngestionSchmuck
from package.haupteil.data_ingestion import DataIngestion

import os, sys


class Pipeline:

  def __init__(self,schmuck: Structure= Structure()) -> None:
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
    

  def run_pipeline(self):
        try:
            data_ingestion_ordner = self.start_data_ingestion()
            
        except Exception as e:
            raise PackageException(e, sys) from e  