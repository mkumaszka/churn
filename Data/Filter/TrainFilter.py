import pickle
import pandas as pd
import os.path as path
import Config.ConfigReader as Config
from multiprocessing import Process

CHUNKSIZE = 1000000


def FilterData(data_to_filter, test_column, condition_set, newfile_name, ch_size):
    """

    :param data_to_filter: filtered data should be in a csv file
    :param test_column: column name that is checked under existance relation:
    :param condition_set set of values for which test_column is being checked:
    :param ch_size: chunk size for file-parsing generator
    """
    generator = pd.read_csv(data_to_filter, chunksize=ch_size)
    headers = pd.read_csv(data_to_filter, nrows=0)
    headers.to_csv(newfile_name, index=False)
    f = open(newfile_name, 'a')
    for chunk in generator:
        filtered = chunk[chunk[test_column].isin(condition_set)]
        filtered.to_csv(newfile_name, mode='a', header=False, index=False)


if __name__ == "__main__":
    train_labels = pickle.load(open(path.join(Config.config['DATA']['data_folder'], 'labels.pkl'), 'rb'))
    ids = list(train_labels.keys())

    data_folder = Config.config['DATA']['data_folder']
    transactions = path.join(data_folder, 'transactions.csv')
    logs = path.join(data_folder, 'user_logs.csv')

    p1 = Process(target=FilterData,
                 args=(transactions, 'msno', ids, path.join(data_folder, 'transactions_filtered.csv'), CHUNKSIZE))
    p2 = Process(target=FilterData,
                 args=(logs, 'msno', ids, path.join(data_folder, 'user_logs_filtered.csv'), CHUNKSIZE))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
