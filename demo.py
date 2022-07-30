from package.pipeline.pipeline import Pipeline
from package.exception import PackageException
from package.logger import logging
from package.structure.structure import structure
from package.haupteil.data_transform import DataTransformation
import os

def main():
    try:
        schmuck_path = os.path.join("schmuck","schmuck.yaml")
        pipeline = Pipeline(structure(schmuck_file_path=schmuck_path))
        print("Hello")
        pipeline = Pipeline()
        #pipeline.run_pipeline()
        pipeline.start()
        logging.info("main function execution completed.")
        #data_validation_ordner = structure().get_data_transformation_schmuck()
        #print(data_validation_ordner)
        
             
    except Exception as e:

        logging.error(f"{e}")
        print(e)



if __name__== "__main__":
     main()
