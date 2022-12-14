import argparse
import glob
from os import rename
from os.path import join, basename, exists
from functions import GetDataFrame, CalcFrequency, CreatePath

#python change_area_types.py --org_type_txt_path "" --new_type 1

AREA_DIVISION = {1:{'1':'1', '2':'1', '3':'2', '4':'3', '5':'3', '6':'4', '7':'5', '8':'5', '9':'6', '10':'7', '11':'7', '12':'8',},
                2:{'1':'1', '2':'0', '3':'0', '4':'0', '5':'0', '6':'0', '7':'0', '8':'0', '9':'0', '10':'0', '11':'0', '12':'0',}}

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple script for changing annotation class.')

    parser.add_argument('--org_type_txt_path', help='Path to .txt file containing .xlsx files path and their class')
    parser.add_argument('--new_type', help='int representing the new area division', type=int)
    parser = parser.parse_args(args)

    assert parser.org_type_txt_path!=None, "org_type_txt_path can't be None"
    assert exists(parser.org_type_txt_path), "org_type_txt_path does not exist"

    if parser.new_type in AREA_DIVISION.keys():
        new_division = AREA_DIVISION[parser.new_type]
        
        f = open(parser.org_type_txt_path)
        data = f.read()
        f.close()

        lines = data.split('\n')
        new_lines = []
        for line in lines:
            f_path, class_type = line.split('\t')
            new_class_type = new_division[class_type]
            new_lines.append(f_path+'\t'+new_class_type)
        f = open(parser.org_type_txt_path,'w')
        f.write('\n'.join(new_lines))
        f.close()
        
if "__main__"==__name__:
    main()