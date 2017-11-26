import numpy as np
import pandas as pd
import Config.ConfigReader as Config
import os.path as path
def create_empty_array(dict_,user_logs):
    length = 0
    for k, v in dict_.items():
        length += len(v) - 1
    shape = (user_logs.shape[0], length)
    return np.zeros(shape)

def generate_bucket(dict_):
    for bucketkey, bucketlist in dict_.items():
        for bucket in bucketlist:
            yield bucket

def generate_log(arr):
    for row in arr:
        for log in row:
            yield log

def create_one_hots_for_user_logs(empty_array, generate_bucket, log_gen, dict_):
    bucket_gen = generate_bucket(dict_)
    lower_bucket = next(bucket_gen)
    upper_bucket = next(bucket_gen)
    log = next(log_gen)
    try:
        for row_index in range(empty_array.shape[0]):
            for column_index in range(empty_array.shape[1]):
                if lower_bucket <= log < upper_bucket:
                    empty_array[row_index, column_index] = 1
                lower_bucket = upper_bucket
                upper_bucket = next(bucket_gen)
                if upper_bucket == 0:
                    log = next(log_gen)
            bucket_gen = generate_bucket(dict_)
    except StopIteration:
        return empty_array


if __name__ == '__main__':
    user_logs = pd.read_csv(path.join(Config.Config['DATA']['data_folder'], 'user_logs.csv'), nrows =3)
    user_logs_np = user_logs.as_matrix()
    #leave out the buckets
    user_logs = user_logs_np[:, 2:]
    dict_ = Config.Config['BUCKETS']['user_logs']

    empty_array = create_empty_array(dict_, user_logs)
    bucket_gen = generate_bucket(dict_)
    log_gen = generate_log(user_logs)
    create_one_hots_for_user_logs(empty_array,generate_bucket ,log_gen, dict_)
    print(empty_array)
