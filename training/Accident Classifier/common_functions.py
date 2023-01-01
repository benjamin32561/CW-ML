import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
import numpy as np
from torch.utils.data import Dataset
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class ClassifierAcceleratorDataset(Dataset):
    def __init__(self, file_list):
        self.files = open(file_list,'r').read().split('\n')
        self.n_files = len(self.files)

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        path, record_class = self.files[idx].split('\t')
        class_to_ret = np.array([float(record_class)])
        df = GetDataFrame(path)
        if as_df:
            return df,class_to_ret
        return df.to_numpy()[:,:-1],class_to_ret