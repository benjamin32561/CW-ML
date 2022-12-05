import argparse
import glob
from os.path import join, exists
from functions import GetDataFrame, PlotRecordData

#python plot_records.py --records_path "C:\\Users\\ben32\\Desktop\\Work\\csv_data\\accidents\\200hz"

def main(args=None):
    parser = argparse.ArgumentParser(description='Script for plotting all records in folder.')

    parser.add_argument('--records_path', help='Path to records folder (contains .csv records)')
    parser = parser.parse_args(args)

    assert parser.records_path!=None, "records_path can't be None"
    assert exists(parser.records_path), "records_path does not exist"

    files = glob.glob(join(parser.records_path,"*.csv"))
    n_files = len(files)
    for idx, file_path in enumerate(files):
        print("{}/{}: {}".format(idx+1,n_files,file_path))
        data = GetDataFrame(file_path)
        PlotRecordData(data,False,False,False)
        
if "__main__"==__name__:
    main()