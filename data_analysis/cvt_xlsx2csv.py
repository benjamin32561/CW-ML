import argparse
import glob
from os.path import join, basename, splitext, exists
from functions import XlsxToCSV, CreatePath

#python cvt_xlsx2csv.py --records_src_path "C:\\Users\\ben32\\Desktop\\Work\\xlsx_data\\not_accidents" --records_dst_path "C:\\Users\\ben32\\Desktop\\Work\\csv_data\\not_accidents"

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple script for converting all .xlsx files to .csv files.')

    parser.add_argument('--records_src_path', help='Path to source records folder (contains .xlsx)')
    parser.add_argument('--records_dst_path', help='Path to save records at (will contain .csv)')
    parser = parser.parse_args(args)

    assert parser.records_src_path!=None, "records_src_path can't be None"
    assert parser.records_dst_path!=None, "records_dst_path can't be None"
    assert exists(parser.records_src_path), "records_src_path does not exist"

    CreatePath(parser.records_dst_path)

    xlsx_files = glob.glob(join(parser.records_src_path,"*.xlsx"))
    n_files = len(xlsx_files)
    for idx, xlsx_file in enumerate(xlsx_files):
        print('',end="\rConverting files... {}/{}".format(idx+1,n_files))
        full_filename = basename(xlsx_file)
        filename, file_ext = splitext(full_filename)
        
        dst_file_path = join(parser.records_dst_path,filename+".csv")

        XlsxToCSV(xlsx_file,dst_file_path)
    print()
        
if "__main__"==__name__:
    main()