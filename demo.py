from package.pipeline.pipeline import Pipeline
from package.exception import HousingException
from package.logger import logging

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
       
       
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()