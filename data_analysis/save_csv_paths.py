import argparse
from random import shuffle
from os.path import exists
from functions import SaveLinesToTxt, GetAllCSVInFolders

#python save_csv_paths.py --folder_class_dict_file C:/Users/ben32/Desktop/work/training/csv_locations.txt --txt_file_location C:\Users\ben32\Desktop\work\data_analysis\folder_class_dict.txt

def main(args=None):
    parser = argparse.ArgumentParser(description='Script for saving all .csv file locations and their class.')

    parser.add_argument('--txt_file_location', help='Path to save final locations file at (.txt)')
    parser.add_argument('--folder_class_dict_file', help="Path to .txt file which specifies each folder and it's class (int/float)")
    parser = parser.parse_args(args)

    assert parser.txt_file_location!=None, "txt_file_location can't be None"
    assert parser.folder_class_dict_file!=None, "folder_class_dict_file can't be None"
    assert exists(parser.folder_class_dict_file), "folder_class_dict_file does not exist"

    f = open(parser.folder_class_dict_file)
    folder_class_dict = f.readlines()
    f.close()

    folders = []
    clas = []
    for idx in range(len(folder_class_dict)):
        line = folder_class_dict[idx]
        folder, current_folder_class = line.split('\t')
        folders.append(folder)
        clas.append(current_folder_class)

    locs = GetAllCSVInFolders(folders,clas)
    shuffle(locs)
    SaveLinesToTxt(locs, parser.txt_file_location)

if __name__=='__main__':
    main()