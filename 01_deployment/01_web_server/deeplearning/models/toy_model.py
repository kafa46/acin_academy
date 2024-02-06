from torch import nn
import torch

class ToyNetwork(nn.Module):
    '''Toy example'''
    def __init__(self, input_size, hidden_size, output_size):
        super(ToyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        '''Forward propagation'''
        return self.fc2(self.relu(self.fc1(x)))

class Train():
    '''Toy Train'''
    def __init__(self) -> None:
        self.model = ToyNetwork(4, 5, 2)

    def run(self,):
        inputs = torch.randn(1, 4)
        output = self.model(inputs)

        # Loss
        print(f'Predict: {output}')
        label = torch.tensor([1.0, 0.0])
        loss = torch.sum((output - label)**2)
        print(f'Loss: {loss}')

        # output.backward(torch.ones_like(output))
        loss.backward()

        gradients = [param.grad for param in self.model.parameters()]

        print('Grandients Test')
        for idx, grad in enumerate(gradients):
            print('---' * 20)
            print(f'Layer {idx}, Shape: {grad.shape[0]}')
            print(grad)

if __name__=='__main__':
    train = Train()
    train.run()