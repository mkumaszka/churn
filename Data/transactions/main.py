import pandas as pd
import pickle as pkl

from Data.transactions.transactions_preprocessing import transactions_to_dataframe_with_one_hots
from Data.transactions.transactions_dict import create_user_dict
from Data.transactions.utils import TRANSACTIONS_CSV_PATH

if __name__ == '__main__':
    transactions = pd.read_csv(TRANSACTIONS_CSV_PATH)
    transactions_preprocessed = transactions_to_dataframe_with_one_hots(transactions)
    transactions_dict = create_user_dict(transactions_preprocessed)
    with open('transactions_processed.pkl', "wb") as file:
        pkl.dump(transactions_dict, file)
