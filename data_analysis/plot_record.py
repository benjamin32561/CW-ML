import argparse
from os.path import exists
from functions import GetDataFrame, PlotRecordData

def main(args=None):
    parser = argparse.ArgumentParser(description='Script for plotting a single record.')

    parser.add_argument('--record_path', help='Path record (.xlsx/.csv)')
    parser = parser.parse_args(args)

    assert parser.record_path!=None, "record_path can't be None"
    assert exists(parser.record_path), "record_path does not exist"

    data = GetDataFrame(parser.record_path)
    PlotRecordData(data, save_to='record.jpg')

        
if "__main__"==__name__:
    main()