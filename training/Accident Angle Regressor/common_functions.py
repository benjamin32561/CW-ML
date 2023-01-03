import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
import numpy as np
from torch import tensor, float32
from torch.utils.data import Dataset
from torch.nn.functional import one_hot
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class RegressionDataset(Dataset):
    def __init__(self, file_list):
        f = open(file_list)
        self.files = f.read().split('\n')
        f.close()

        self.n_files = len(self.files)

    def __len__(self):
        return self.n_files

    def GetDFAndClass(self, file_path:str, as_df=False):
        path, record_angle = file_path.split('\t')
        angle_to_ret = np.array([float(record_angle)/360])
        df = GetDataFrame(path)
        if not as_df:
            df = df.to_numpy()[:,:-1]
        return df,angle_to_ret

    def __getitem__(self, idx, as_df=False):
        files = self.files[idx]
        if type(files)==list:
            to_ret = []
            for f_path in self.files[idx]:
                df,acc_angle = self.GetDFAndClass(f_path,as_df)
                to_ret.append((df,acc_angle))
            return to_ret
        return self.GetDFAndClass(files,as_df)