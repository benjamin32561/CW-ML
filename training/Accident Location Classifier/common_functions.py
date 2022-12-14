import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
import numpy as np
from torch import tensor, float32
from torch.utils.data import Dataset
from torch.nn.functional import one_hot
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class AccidentLocationClassifierAcceleratorDataset(Dataset):
    def __init__(self, file_list, num_class):
        f = open(file_list)
        self.files = f.read().split('\n')
        f.close()
        self.n_files = len(self.files)
        self.nc = num_class

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        path, record_class = self.files[idx].split('\t')
        class_to_ret = np.array([int(record_class)-1])
        one_hot_enc_to_ret = one_hot(tensor(class_to_ret),num_classes=self.nc).to(float32)
        df = GetDataFrame(path)
        print(one_hot_enc_to_ret.size())
        if as_df:
            return df,one_hot_enc_to_ret
        return df.to_numpy()[:,:-1],one_hot_enc_to_ret