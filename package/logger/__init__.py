from datetime import datetime
import logging
import os
from datetime import datetime

LOG_DIR= "Travel_logs"

CURRENT_TIME_STEMP= f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"

log_file_name= f"log{CURRENT_TIME_STEMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_file_path= os.path.join(LOG_DIR,log_file_name)

logging.basicConfig(filename=log_file_path,
filemode="w",
format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
level=logging.INFO
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]
