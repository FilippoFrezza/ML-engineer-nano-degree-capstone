import torch
from torch.autograd import Variable
import torch.nn.functional as F

class RegNet(torch.nn.Module):
    
    #def __init__(self, n_feature, n_hidden, n_output):
        #self.n_feature = n_feature
        #super(RegNet, self).__init__()
        #self.hidden = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        #self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer
    def __init__(self, inputSize, outputSize):
        super(RegNet, self).__init__()
        self.inputSize = inputSize
        self.outputSize = outputSize
        
        self.fc1 = torch.nn.Linear(inputSize, 128)
        self.fc2 = torch.nn.Linear(128, outputSize)

    def forward(self, x):
        x = x.view(-1, self.inputSize)
        #x = F.relu(self.hidden(x))      # activation function for hidden layer
        #x = self.predict(x)             # linear output
        #return x
   
        #x = F.relu(self.fc2(F.relu(self.fc1(x))))
        x = self.fc2(self.fc1(x))
        
        return x