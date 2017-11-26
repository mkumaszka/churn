import numpy as np
import pandas as pd

import Config.ConfigReader as config

class Process:

    dict_ = config.config['BUCKETS']['user_logs']

    def process_user_logs(self,data):
        data = self.create_buckets(data)
        data = self.data_to_dictionary(data)
        data = self.clear_dict(data)
        return data

    def create_buckets(self, data):
        one_hot_logs = self.create_one_hot(self.take_logs(data))
        usernames = data['msno']
        dates = data['date']
        logs = self.to_dataframe(one_hot_logs)
        to_concat = [usernames,dates,logs]
        return self.concatenate_columns(to_concat)

    def to_dataframe(self, one_hot_logs):
        df = pd.DataFrame()
        df['buckets'] = one_hot_logs.tolist()
        return df

    def create_one_hot(self, user_logs):
        empty_array = self.create_empty_array(self.dict_, user_logs)
        log_gen = self.generate_log(user_logs)
        return self.create_one_hots_for_user_logs(empty_array, self.generate_bucket, log_gen, self.dict_)

    def take_logs(self, data):
        user_logs_np = data.as_matrix()
        user_logs = user_logs_np[:, 2:]
        return user_logs

    def create_empty_array(self,dict_, user_logs):
        length = 0
        for k, v in dict_.items():
            length += len(v) - 1
        shape = (user_logs.shape[0], length)
        return np.zeros(shape)

    def generate_bucket(self,dict_):
        for bucketkey, bucketlist in dict_.items():
            for bucket in bucketlist:
                yield bucket

    def generate_log(self,arr):
        for row in arr:
            for log in row:
                yield log

    def create_one_hots_for_user_logs(self,empty_array, generate_bucket, log_gen, dict_):
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

        return empty_array

    def concatenate_columns(self, columns):
        return pd.concat(columns, axis=1)

    def data_to_dictionary(self, df):
        "Create dictionary. Use msno values as keys and add a list of (date, one-hot) tuples to the specific key value"
        msnoDict = {}
        msnoList = []
        for userID in df["msno"]:
            if userID in msnoList:
                pass
            else:
                msnoDf = df[df["msno"] == userID]
                tuplesList = []
                for index, row in msnoDf.iterrows():
                    date = row["date"]
                    row = row.drop(["msno", "date"])
                    onehotList = list(row)
                    singleTuple = (date, onehotList)
                    tuplesList.append(singleTuple)

                msnoList.append(userID)
                msnoDict[userID] = tuplesList

        return msnoDict

    def sort_list_by_dates(self,list):
        list.sort(key=lambda tup: tup[0])
        return list

    def remove_dates(self,list):
        return [elem[1] for elem in list]

    def sort_dict_by_dates(self,dictionary):
        return {k: self.sort_list_by_dates(v) for k, v in dictionary.items()}

    def remove_dates_from_dict(self,dictionary):
        return {k: self.remove_dates(v) for k, v in dictionary.items()}

    def clear_dict(self,dictionary):
        return self.remove_dates_from_dict(self.sort_dict_by_dates(dictionary))

