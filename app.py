from this import s
from flask import Flask, request
import sys

import pip
from package.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from package.logger import logging
from package.exception import PackageException
import os, sys
import json
from package.structure.structure import structure
from package.bestandteil import SCHMUCK_DIR, get_current_time_stamp
from package.pipeline.pipeline import Pipeline
from package.gebilde.package_predictor import PackagePredictor, PackageData
from flask import send_file, abort, render_template


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "package"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_SCHMUCK_FILE_PATH = os.path.join(ROOT_DIR, SCHMUCK_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
from package.logger import get_log_dataframe


PACKAGE_DATA_KEY = "package_data"
PRODTAKEN_KEY = "ProdTaken"

app = Flask(__name__)

@app.route('/ordner', defaults={'class_path': 'Package'})
@app.route('/ordner/<path:class_path>')

def render_ordner_dir(class_path):
    os.makedirs("package", exist_ok=True)
    # Joining the base and the requested path
    print(f"class_path: {class_path}")
    abs_path = os.path.join(class_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "ordner" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():

    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(schmuck=structure(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        PACKAGE_DATA_KEY: None,
        PRODTAKEN_KEY: None
    }

    if request.method == 'POST':
          Age = float(request.form['Age'])
          TypeofContact =request.form['TypeofContact']
          CityTier        = int(request.form['CityTier'])
          DurationOfPitch = float(request.form['DurationOfPitch '])
          Occupation      =  request.form['Occupation']  
          Gender          =  request.form['Gender']   
          NumberOfPersonVisiting = int(request.form['NumberOfPersonVisiting'])
          NumberOfFollowups = float(request.form['NumberOfFollowups'])
          PreferredPropertyStar =float(request.form['PreferredPropertyStar'])
          MaritalStatus  =   request.form['MaritalStatus']
          NumberOfTrips  =  float(request.form['umberOfTrips'])   
          Passport       =   int(request.form['Passport'])   
          ProductPitched  =   request.form['ProductPitched']      
          PitchSatisfactionScore  = int(request.form['PitchSatisfactionScore'])   
          OwnCar                  = int(request.form['OwnCar'])   
          NumberOfChildrenVisiting =float(request.form['umberOfChildrenVisiting'])   
          Designation   = request.form['Designation']
          MonthlyIncome  = float(request.form['MonthlyIncome'])   


          package_data = PackageData(Age = Age,
                                   TypofContact =TypeofContact,  
                                    CityTier =CityTier,
                                    DurationOfPitch=DurationOfPitch,
                                     Occupation=Occupation,
                                    Gender =Gender,
                                    NumberOfPersonVisiting=NumberOfPersonVisiting,
                                    NumberOfFollowups=NumberOfFollowups,
                                    PreferredPropertyStar=PreferredPropertyStar,
                                    MaritalStatus = MaritalStatus,
                                     NumberOfTrips =NumberOfTrips,
                                    Passport =Passport,
                                     ProductPitched = ProductPitched,
                                      PitchSatisfactionScore = PitchSatisfactionScore,
                                     OwnCar = OwnCar,  
                                    NumberOfChildrenVisiting = NumberOfChildrenVisiting,
                                    Designation =  Designation, 
                                    MonthlyIncome = MonthlyIncome 
                                   )
          package_df = package_data.get_package_input_data_frame()
          package_predictor = PackagePredictor(model_dir=MODEL_DIR)
          ProdTaken= package_predictor.predict(X=package_df)
          context = {
            PACKAGE_DATA_KEY: package_data.get_package_data_as_dict(),
            PRODTAKEN_KEY: ProdTaken,
             }
          return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)

@app.route('/saved_models', defaults={'class_path': 'saved_models'})
@app.route('/saved_models/<path:class_path>')
def saved_models_dir(class_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"class_path: {class_path}")
    abs_path = os.path.join(class_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    
    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_schmuck", methods=['GET', 'POST'])
def update_model_schmuck():
    try:
        if request.method == 'POST':
            model_schmuck = request.form['new_model_schmuck']
            model_schmuck = model_schmuck.replace("'", '"')
            print(model_schmuck)
            model_schmuck = json.loads(model_schmuck)

            write_yaml_file(file_path=MODEL_SCHMUCK_FILE_PATH, data=model_schmuck)

        model_schmuck = read_yaml_file(file_path=MODEL_SCHMUCK_FILE_PATH)
        return render_template('update_model.html', result={"model_schmuck": model_schmuck})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'class_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:class_path>')
def render_log_dir(class_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {class_path}")
    abs_path = os.path.join(class_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()