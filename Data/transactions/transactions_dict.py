from Data.transactions.transactions_preprocessing import sort_by_column

def create_user_dict(dataframe):
    usernames = dataframe['msno'].unique()
    users = {}
    users = users.fromkeys(usernames)
    for username in usernames:
        users[username] = []
        user_list = users[username]
        selected_users = dataframe[(dataframe['msno'] == username)]
        selected_users_sorted_by_date = sort_by_column(selected_users, 'transaction_date')
        selected_users_ = selected_users_sorted_by_date.iterrows()
        for _ in range(selected_users_sorted_by_date.shape[0]):
            user_transaction = next(selected_users_)[1]
            user_transaction_date = user_transaction['transaction_date']
            user_transactions_columns = user_transaction.drop('transaction_date').drop('msno')
            user_list.append((user_transaction_date, user_transactions_columns.values.tolist()))

    return users

