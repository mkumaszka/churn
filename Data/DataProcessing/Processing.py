import pandas as pd
import pickle as pkl
import Data.DataProcessing.Process as Process
import Config.ConfigReader as config
import os.path as path

processer = Process.Process()

def process_raw_data(raw_data):
    return processer.process_user_logs(raw_data)


if __name__ == '__main__':
    user_logs = pd.read_csv(path.join(config.config['DATA']['data_folder'], 'user_logs.csv'), nrows =3)
    preprocessed_user_logs = process_raw_data(user_logs)
    print(preprocessed_user_logs)
    with open('user_logs_processed.pkl', "wb") as file:
        pkl.dump(preprocessed_user_logs, file)

