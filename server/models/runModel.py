import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import pandas as pd
import csv

#ported from notebook
class ComplexityDataset(Dataset):
    def __init__(self, csv_file: str):

        df = pd.read_csv(csv_file)
        df = df.drop(labels = "id", axis=1)
        self.X = df.drop(labels = "heat", axis=1)
        self.y = df["heat"]
        
    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        # Convert idx from tensor to list due to pandas bug (that arises when using pytorch's random_split)
        if isinstance(idx, torch.Tensor):
            idx = idx.tolist()

        return [self.X.iloc[idx].values, self.y[idx]]

class ComplexityNN(nn.Module):

    def __init__(self, D_in, D_out=1):
        super().__init__()
        self.fc1 = nn.Linear(D_in, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, D_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x.squeeze()


def runInferenceModel(modelPath:str, inferenceFile:str)->list:
    """
    Given a csv of inputs, returns a list of heatVals
    """
    model = torch.load(modelPath, map_location=torch.device('cpu'))
    model.eval()
    heatVals = []
    with open(inferenceFile, newline='') as dsFile:
        dsReader = csv.reader(dsFile, delimiter = ',', quotechar='|')
        next(dsReader)
        for row in dsReader:
            features = [float(feature) for feature in row[2:]]
            inferenceTensor = torch.Tensor(features)
            inferenceTensor = torch.reshape(inferenceTensor, (len(features), 1))
            output = model(inferenceTensor)
            heatVal = round(sum(output.tolist())/output.size()[0], 2)
            heatVals.append(heatVal)
    return heatVals
    
            

runInferenceModel('model.pt', 'inferenceTable.csv')