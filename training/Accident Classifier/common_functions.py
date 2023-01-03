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

    def GetDFAndClass(self, file_path:str,as_df=False):
        path, record_class = file_path.split('\t')
        class_to_ret = np.array([float(record_class)])
        df = GetDataFrame(path)
        if not as_df:
            df = df.to_numpy()[:,:-1]
        return df,class_to_ret

    def __getitem__(self, idx, as_df=False):
        files = self.files[idx]
        if type(files)==list:
            to_ret = []
            for file_path in files:
                df, class_to_ret = self.GetDFAndClass(file_path,as_df)
                to_ret.append((df,class_to_ret))
            return to_ret
        return self.GetDFAndClass(files,as_df)