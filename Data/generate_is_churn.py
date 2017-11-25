import pandas as pd
import datetime
import csv

datestr = datetime.datetime.strptime
CHUNK = 100000
generative_columns = ["msno", "transaction_date", "membership_expire_date"]
reader = pd.read_csv("DATA/transactions.csv", usecols=generative_columns, chunksize=CHUNK)
user_data = dict()
churn_data = []
churn_data.append(["msno", "is_churn"])


def addtoDict(chunk):
    user = chunk.iloc[0]
    single_log = chunk.iloc[1:].tolist()
    if user not in user_data:
        user_data[user] = []
    user_data[user].append(single_log)


def calculateChurn(dataframe):
    if len(dataframe) > 1:
        dataframe.sort(key=lambda log: log[0])
        for i in range(len(dataframe) - 1):
            expire_date = datestr(str(dataframe[i][1]), "%Y%m%d")
            new_subscription = datestr(str(dataframe[i + 1][0]), "%Y%m%d")
            difference = (new_subscription - expire_date).days
            if difference > 30:
                return 1
    else:
        return 0
    return 0


# aggregate data for every user
for chunk in reader:
    chunk.apply(addtoDict, axis=1, raw=True)
print("Done aggregating\n")

# calculate churn for every user
unique_users_number = len(user_data)
print("Number of unique users: ", unique_users_number)
user_count = 0
for user, dataframe in user_data.items():
    if user_count % 10000 == 0:
        print(user_count)
    user_count += 1
    churn_data.append([user, calculateChurn(dataframe)])

with open("is_churn_generated.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(churn_data)
