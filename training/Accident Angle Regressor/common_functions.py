import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
import numpy as np
from torch import tensor, float32
from torch.utils.data import Dataset
from torch.nn.functional import one_hot
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class AccidentAngleAcceleratorDataset(Dataset):
    def __init__(self, file_list):
        f = open(file_list)
        self.files = f.read().split('\n')
        f.close()
        self.n_files = len(self.files)

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        path, record_class = self.files[idx].split('\t')
        angle_to_ret = np.array([float(record_class)])
        df = GetDataFrame(path)
        if as_df:
            return df,angle_to_ret
        return df.to_numpy()[:,:-1],angle_to_ret