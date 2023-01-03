import sys
import os
sys.path.append(os.path.abspath('/content/Cloud-Wise-ML/'))
from torch.utils.data import Dataset
from glob import glob
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class AEAcceleratorDataset(Dataset):
    def __init__(self, file_list):
        self.file_list = file_list
        self.n_files = len(self.file_list)

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        files_to_ret = self.file_list[idx]
        if type(files_to_ret)==list:
            df_to_ret = []
            for file_to_ret in files_to_ret:
                df_to_ret.append(GetDataFrame(file_to_ret))
            if as_df:
                return df_to_ret
            return [df.to_numpy()[:,:-1] for df in df_to_ret]
        df = GetDataFrame(files_to_ret)
        if as_df:
            return df
        return df.to_numpy()[:,:-1]