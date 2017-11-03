import datetime

timestamps = ['2011-06-2', '2011-08-05', '2011-02-04', '2010-1-14', '2010-12-13', '2010-1-12', '2010-2-11', '2010-2-07',
              '2010-12-02', '2011-11-30', '2010-11-26', '2010-11-23', '2010-11-22', '2010-11-16']

dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in timestamps]

bucket1 = [[0, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]]
bucket2 = [[0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [0, 1, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
bucket3 = [[1, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0]]

user1_val = [(dates[2], bucket1), (dates[3], bucket2), (dates[4], bucket3)]
user2_val = [(dates[3], bucket1), (dates[4], bucket2), (dates[5], bucket3)]

dict1 = {1: user1_val, 2: user2_val}


def sort_list_by_dates(list):
    list.sort(key=lambda tup: tup[0])
    return list


def remove_dates(list):
    return [elem[1] for elem in list]


def sort_dict_by_dates(dictionary):
    return {k: sort_list_by_dates(v) for k, v in dictionary.items()}


def remove_dates_from_dict(dictionary):
    return {k: remove_dates(v) for k, v in dictionary.items()}


def clear_dict(dictionary):
    return remove_dates_from_dict(sort_dict_by_dates(dictionary))


print(clear_dict(dict1))
