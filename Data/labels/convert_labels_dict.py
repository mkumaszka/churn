import Config.ConfigReader as Config
import os.path as path
import pandas as pd
import pickle as pkl

labels = pd.read_csv(path.join(Config.config['DATA']['data_folder'], 'train.csv'))

labels_dict = dict([(msno, bool(is_churn)) for msno, is_churn in zip(labels.msno, labels.is_churn)])
with open('labels.pkl', "wb") as file:
    pkl.dump(labels_dict, file)
