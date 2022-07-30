import os
import sys

from package.exception import PackageException
from package.util.util import load_object

import pandas as pd


class PackageData:

    def __init__(self,
                 Age : float,
                 TypeofContact   : str,
                 CityTier        : int,
                 DurationOfPitch : float,
                 Occupation      :  str,       
                 Gender          :   str,       
                 NumberOfPersonVisiting : int,
                 NumberOfFollowups : float,
                 PreferredPropertyStar : float,
                 MaritalStatus  :  str,       
                 NumberOfTrips  :  float,
                 Passport       :   int,
                 ProductPitched  :  str,         
                 PitchSatisfactionScore  : int,
                 OwnCar                  : int,
                 NumberOfChildrenVisiting  :float,
                 Designation   :   str, 
                 MonthlyIncome  :   float,
                 ProdTaken   :  int = None
                 ):

        try:
            self.Age = Age
            self.TypofContact =TypeofContact   
            self.CityTier =CityTier
            self.DurationOfPitch=DurationOfPitch
            self.Occupation=Occupation
            self.Gender =Gender  
            self.NumberOfPersonVisiting=NumberOfPersonVisiting
            self.NumberOfFollowups=NumberOfFollowups
            self.PreferredPropertyStar=PreferredPropertyStar
            self.MaritalStatus = MaritalStatus 
            self.NumberOfTrips =NumberOfTrips 
            self.Passport = Passport 
            self.ProductPitched = ProductPitched
            self.PitchSatisfactionScore = PitchSatisfactionScore
            self.OwnCar = OwnCar  
            self.NumberOfChildrenVisiting = NumberOfChildrenVisiting
            self.Designation =  Designation 
            self.MonthlyIncome = MonthlyIncome 
            self.ProdTaken  = ProdTaken 

           
        except Exception as e:
            raise PackageException(e, sys) from e

    def get_package_input_data_frame(self):

        try:
            package_input_dict = self.get_package_data_as_dict()
            return pd.DataFrame(package_input_dict)
        except Exception as e:
            raise PackageException(e, sys) from e

    def get_package_data_as_dict(self):
        try:
            input_data = {"Age": [self.Age],
                         "TypofContact": [self.TypofContact],
                         "CityTier": [self.CityTier],
                        "DurationOfPitch": [self.DurationOfPitch],
                         "Occupation": [self.Occupation],
                         "Gender": [self.Gender],
                         "NumberOfPersonVisiting": [self.NumberOfPersonVisiting],
                         "NumberOfFollowups": [self.NumberOfFollowups],
                         "ProductPitched":[self.ProductPitched],
                         "PreferredPropertyStar":[self.PreferredPropertyStar],
                          "MaritalStatus":[self.MaritalStatus],
                          "NumberOfTrips":[self.NumberOfTrips],
                          " Passport ":[self. Passport ],
                          "PitchSatisfactionScore ":[self.PitchSatisfactionScore ],
                           "OwnCar ":[self.OwnCar ],
                            "NumberOfChildrenVisiting ":[self.NumberOfChildrenVisiting ],
                           "Designation":[self.Designation ],
                            "MonthlyIncome":[self.MonthlyIncome]}
            return input_data
        except Exception as e:
            raise PackageException(e, sys)


class PackagePredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise PackageException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise PackageException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            ProdTaken = model.predict(X)
            return ProdTaken
        except Exception as e:
            raise PackageException(e, sys) from e