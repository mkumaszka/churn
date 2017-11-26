import numpy as np
import pandas as pd


def drop_column(column_name, dataframe):
    return dataframe.drop(column_name, axis=1)

def column_to_one_hot(column_index, np_array):
    return pd.get_dummies(np_array[:, column_index]).values

def consecutive_columns_to_one_hot(range, np_array):
    columns_in_one_hot = []
    for column_index in range:
        columns_in_one_hot.append(column_to_one_hot(column_index, np_array))
    return columns_in_one_hot

def concatenate_one_hot_columns(columns):
    concatenated = np.concatenate((columns[0], columns[1]), axis=1)
    for column_indx in range(2, len(columns)):
        concatenated = np.concatenate((concatenated, columns[column_indx]), axis=1)
    return concatenated

def to_dataframe(np_array):
    return pd.DataFrame(np_array)

def concatenate_columns_df(columns):
    return pd.concat(columns, axis=1)

def sort_by_column(dataframe, column):
    return dataframe.sort_values(column, axis=0)

def column_to_datetime(column):
    return pd.to_datetime(column.astype(str), format='%Y%m%d')


def transactions_to_dataframe_with_one_hots(transactions):
    transaction_date = transactions['transaction_date']
    transaction_date = column_to_datetime(transaction_date)
    username = transactions['msno']
    transactions = drop_column('membership_expire_date', transactions)
    transactions = drop_column('transaction_date', transactions)
    transactions = sort_by_column(transactions, 'msno')
    transactions_np = transactions.values
    one_hot_columns = consecutive_columns_to_one_hot(range(1,4), transactions_np)
    concatenated_one_hots = concatenate_one_hot_columns(one_hot_columns)
    concatenated_one_hots = to_dataframe(concatenated_one_hots)
    to_concat = [username, transaction_date, concatenated_one_hots]
    return concatenate_columns_df(to_concat)
