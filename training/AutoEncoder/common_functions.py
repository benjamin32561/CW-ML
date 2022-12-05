import sys
import os
sys.path.append(os.path.abspath('../../'))
from torch.utils.data import Dataset
from data_analysis.functions import GetDataFrame, PlotRecordData, CreatePath

class AEAcceleratorDataset(Dataset):
    def __init__(self, csv_file_list):
        """
        Args:
            csv_file_list (string): Paths to .txt which contains all recordings paths.
        """
        self.csv_file_list = open(csv_file_list,'r').read().split('\n')[:10]
        self.n_files = len(self.csv_file_list)

    def __len__(self):
        return self.n_files

    def __getitem__(self, idx, as_df=False):
        df = GetDataFrame(self.csv_file_list[idx].split('\t')[0])
        if as_df:
            return df
        return df.to_numpy()[:,:-1]