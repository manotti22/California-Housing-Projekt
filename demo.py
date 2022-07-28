from package.pipeline.pipeline import Pipeline
from package.exception import PackageException
from package.logger import logging
from package.structure.structure import structure

def main():
    try:
        print("Hello")
        #pipeline = Pipeline()
        #pipeline.run_pipeline()
        data_validation_ordner = structure().get_data_transformation_schmuck()
        print(data_validation_ordner)
        
             
    except Exception as e:

        logging.error(f"{e}")
        print(e)



if __name__== "__main__":
     main()
