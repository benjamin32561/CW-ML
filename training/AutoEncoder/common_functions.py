import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
from torch.utils.data import Dataset
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class AEAcceleratorDataset(Dataset):
    def __init__(self, file_list):
        self.file_list = open(file_list,'r').read().split('\n')
        self.n_files = len(self.file_list)

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        df = GetDataFrame(self.file_list[idx].split('\t')[0])
        if as_df:
            return df
        return df.to_numpy()[:,:-1]