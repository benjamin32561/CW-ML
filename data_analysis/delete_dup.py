import argparse
from random import shuffle
from os.path import exists
from functions import DeleteDuplicates

#python delete_dup.py --folders_spec_file ""

def main(args=None):
    parser = argparse.ArgumentParser(description='Script for saving all .xlsx file locations and their class.')

    parser.add_argument('--folders_spec_file', help='Path to file that specifies the folder to find dups in and flders to check files from (.txt)')
    parser = parser.parse_args(args)

    assert parser.folders_spec_file!=None, "folders_spec_file can't be None"
    assert exists(parser.folders_spec_file), "folders_spec_file does not exist"

    f = open(parser.folders_spec_file)
    folder_class_dict = f.read().split('\n')
    f.close()

    check_from_folders = folder_class_dict[:-2]
    check_in_folder = folder_class_dict[-1]
    
    n_folders = len(check_from_folders)
    for idx in range(n_folders):
        print(f"\r{idx+1}/{n_folders} folders",end='')
        DeleteDuplicates(check_from_folders[idx], check_in_folder)

if __name__=='__main__':
    main()