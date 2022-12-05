import argparse
from os.path import basename,dirname, join, exists
from functions import SaveLinesToTxt

TRAIN_TEST_SPLIT = {'train_':0.8,'test_':0.2}

#python split_txt.py --txt_file_location C:\Users\ben32\Desktop\work\training\csv_locations.txt

def main(args=None):
    parser = argparse.ArgumentParser(description='Script for spliting .txt file to train.txt and test.txt.')

    parser.add_argument('--txt_file_location', help='Path to .txt file')
    parser = parser.parse_args(args)

    assert parser.txt_file_location!=None, "txt_file_location can't be None"
    assert exists(parser.txt_file_location), "txt_file_location does not exist"
    assert sum(TRAIN_TEST_SPLIT.values())==1.0, 'Train Test Split must sum to 1'

    directory = dirname(parser.txt_file_location)
    filename = basename(parser.txt_file_location)
    lines = open(parser.txt_file_location).read().split('\n')
    n_lines = len(lines)
    last_idx = 0
    for phase in TRAIN_TEST_SPLIT.keys():
        new_file = join(directory,phase+filename)
        n_phase_lines = int(n_lines*TRAIN_TEST_SPLIT[phase])
        phase_lines = lines[last_idx:last_idx+n_phase_lines]
        SaveLinesToTxt(phase_lines,new_file)

if __name__=='__main__':
    main()