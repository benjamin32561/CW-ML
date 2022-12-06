import argparse
import glob
from os import rename
from os.path import join, basename, exists
from functions import GetDataFrame, CalcFrequency, CreatePath

#python split_hz.py --records_path "C:\\Users\\ben32\\Desktop\\Work\\csv_data\\accidents"

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple script for splitting all recird in folder to 200hz and 400hz folders.')

    parser.add_argument('--records_path', help='Path to recordings folder (contains .xlsx records)')
    parser = parser.parse_args(args)

    assert parser.records_path!=None, "records_path can't be None"
    assert exists(parser.records_path), "records_path does not exist"

    th_hz_folder_path = join(parser.records_path,"200hz")
    fh_hz_folder_path = join(parser.records_path,"400hz")

    CreatePath(th_hz_folder_path)
    CreatePath(fh_hz_folder_path)

    files = glob.glob(join(parser.records_path,"*.xlsx"))
    n_files = len(files)
    for idx, file_path in enumerate(files):
        print("",end="\rTransfering files: {}/{}".format(idx+1,n_files))
        full_filename = basename(file_path)
        df = GetDataFrame(file_path)
        freq = CalcFrequency(df)
        new_file_path = file_path
        if freq==200:
            new_file_path = join(th_hz_folder_path,full_filename)
        elif freq==400:
            new_file_path = join(fh_hz_folder_path,full_filename)
        rename(file_path,new_file_path)
    print()
        
if "__main__"==__name__:
    main()