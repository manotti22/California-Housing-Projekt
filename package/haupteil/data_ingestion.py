from package.gebilde.schmuck_gebilde import DataIngestionSchmuck
import sys,os
from package.exception import PackageException
from package.logger import logging
from package.gebilde.ordner_gebilde import DataIngestionOrdner
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_ordner:DataIngestionSchmuck ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_ordner = data_ingestion_ordner

        except Exception as e:
            raise PackageException(e,sys)
    

    def download_package_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_ordner.dataset_download_url

            #folder location to download file
            tgz_download_dir = self.data_ingestion_ordner.tgz_download_dir
            
            os.makedirs(tgz_download_dir,exist_ok=True)

            Package_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, Package_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path

        except Exception as e:
            raise PackageException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_ordner.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as package_tgz_file_obj:
                package_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")

        except Exception as e:
            raise PackageException(e,sys) from e
    
    def split_data_as_train_test(self) -> DataIngestionOrdner:
        try:
            raw_data_dir = self.data_ingestion_ordner.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            package_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{package_file_path}]")
            package_data_frame = pd.read_csv(package_file_path)

            package_data_frame["ProdTaken_cat"] = pd.cut(
                package_data_frame["ProdTaken"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(package_data_frame, package_data_frame["ProdTaken_cat"]):
                strat_train_set = package_data_frame.loc[train_index].drop(["ProdTaken_cat"],axis=1)
                strat_test_set = package_data_frame.loc[test_index].drop(["ProdTaken_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_ordner.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_ordner.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_ordner.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_ordner.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_ordner = DataIngestionOrdner(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_ordner}]")
            return data_ingestion_ordner

        except Exception as e:
            raise PackageException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionOrdner:
        try:
            tgz_file_path =  self.download_package_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise PackageException(e,sys) from e
    


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")