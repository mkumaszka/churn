import Config.ConfigReader as Config
import Model.network as network
import torch
from torch.autograd import Variable

transaction_str = Config.config['NET']['Dense']['transactions_structure']
logs_str = Config.config['NET']['Dense']['logs_structure']

p = network.Net(transaction_str, logs_str)
x = Variable(torch.FloatTensor([[0, 1, 0, 1, 1]]))
t = p.forward((x, 'L'))
print(t.grad_fn)
