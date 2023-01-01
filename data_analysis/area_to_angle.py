import argparse
import glob
from os import rename
from os.path import join, basename, exists
from functions import GetDataFrame, CalcFrequency, CreatePath

#python change_area_types.py --org_type_txt_path ""

AREA_TO_ANGLE = {'1':45, '2':67.5, '3':90, '4':112.5, '5':135, '6':180, '7':225, '8':247.5, '9':270, '10':292.5, '11':315, '12':360}

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple script for changing annotation class.')

    parser.add_argument('--org_type_txt_path', help='Path to .txt file containing .xlsx files path and their class')
    parser = parser.parse_args(args)

    assert parser.org_type_txt_path!=None, "org_type_txt_path can't be None"
    assert exists(parser.org_type_txt_path), "org_type_txt_path does not exist"
        
    f = open(parser.org_type_txt_path)
    data = f.read()
    f.close()

    lines = data.split('\n')
    new_lines = []
    for line in lines:
        f_path, class_type = line.split('\t')
        angle = AREA_TO_ANGLE[class_type]
        new_lines.append(f_path+'\t'+str(angle))
    f = open(parser.org_type_txt_path,'w')
    f.write('\n'.join(new_lines))
    f.close()
        
if "__main__"==__name__:
    main()