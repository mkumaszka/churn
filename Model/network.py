import torch
import torch.nn as nn
import torch.nn.functional as F
import Config.ConfigReader as Config

dense_activation = Config.config['NET']['Dense']['activation']
dense_activation = getattr(nn.functional, dense_activation)


class Net(nn.Module):
    def __init__(self, transactions_structure, logs_structure):
        super(Net, self).__init__()
        self.dense_transactions = nn.ModuleList()
        self.dense_user_logs = nn.ModuleList()

        self.createDense(transactions_structure, 'transactions', self.dense_transactions)
        self.createDense(logs_structure, 'user_logs', self.dense_user_logs)

    def createDense(self, structure, part_name, module_list):
        for layer, position in zip(structure[:-1], range(len(structure) - 1)):
            current_module = nn.Linear(structure[position], structure[position + 1])
            module_list.append(current_module)
        return

    def forward(self, x):
        data = x[0]
        flag = x[-1]
        if flag == 'T':
            for _, p in enumerate(self.dense_transactions):
                data = p(data)
                data = dense_activation(data)
        elif flag == 'L':
            for _, p in enumerate(self.dense_user_logs):
                data = p(data)
                data = dense_activation(data)
        else:
            raise ValueError('Unknown data flag')
        return data
