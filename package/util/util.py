import yaml 
from package.exception import PackageException
import os,sys
import numpy as np
import dill 
import pandas as pd 
from package.bestandteil import *


def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise PackageException(e,sys)



def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise PackageException(e,sys) from e