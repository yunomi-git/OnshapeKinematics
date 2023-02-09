import torch
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import UpperConfidenceBound
from botorch.optim import optimize_acqf
import matplotlib.pyplot as plt

def costFunction(x):
    # y += 0.1 * torch.rand_like(y)
    return -torch.square(x.norm(dim=-1, keepdim=True)) * 5

train_X = torch.rand(10, 2) - 0.5
train_Y = costFunction(train_X)
print(train_Y)
print(train_Y.size())

for i in range(10):
    gp = SingleTaskGP(train_X, train_Y)
    mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
    fit_gpytorch_mll(mll);

    UCB = UpperConfidenceBound(gp, beta=0.1)

    bounds = torch.stack([torch.zeros(2), torch.ones(2)])
    candidate, acq_value = optimize_acqf(
        UCB, bounds=bounds, q=1, num_restarts=5, raw_samples=20,
    )

    train_X = torch.cat((train_X, candidate))
    newY = costFunction(candidate)
    print(newY)
    print(newY.size())
    train_Y = torch.cat((train_Y, newY))

plt.plot(train_X[:,0], train_X[:,1])
plt.show()

print(train_X[:,0])
print(train_X[:,1])