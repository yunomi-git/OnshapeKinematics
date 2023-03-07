import torch


class ParameterBounds:
    def __init__(self):
        self.bounds = None

    def addBound(self, min, max):
        newBound = torch.Tensor([[min],[max]])
        if self.bounds is None:
            self.bounds = newBound
        else:
            self.bounds = torch.cat((self.bounds, newBound), dim=1)
        # bounds = torch.stack([torch.ones(self.parameterDimensions) * -boundsMagnitude,
        #                       torch.ones(self.parameterDimensions) * boundsMagnitude]).double()