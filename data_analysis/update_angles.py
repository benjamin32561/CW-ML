import argparse
import glob
from os import rename
from os.path import join, basename, exists
from functions import GetDataFrame, CalcFrequency, CreatePath

#python update_angles.py --angles_txt_path "" --time_to_angle_txt_path ""

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple script for changing recording accident angle.')

    parser.add_argument('--angles_txt_path', help='Path to .txt file containing .xlsx files path and their angles')
    parser.add_argument('--time_to_angle_txt_path', help='Path to .txt file containing units, time and new angle')
    parser = parser.parse_args(args)

    assert parser.angles_txt_path!=None, "angles_txt_path can't be None"
    assert exists(parser.angles_txt_path), "angles_txt_path does not exist"
    assert parser.time_to_angle_txt_path!=None, "time_to_angle_txt_path can't be None"
    assert exists(parser.time_to_angle_txt_path), "time_to_angle_txt_path does not exist"
        
    f = open(parser.angles_txt_path)
    recordings_and_angles = f.read().split('\n')
    f.close()
    n_recordings = len(recordings_and_angles)

    f = open(parser.time_to_angle_txt_path)
    lines = f.read().split('\n')
    f.close()
    angle_by_time = {}
    for line in lines:
        units,time,angle = line.split(' ')
        units = units.split(',')
        angle_by_time[time]={"angle":angle,"units":units}
    
    for i in range(n_recordings):
        recording = recordings_and_angles[i]
        path, recording_angle = recording.split('\t')
        for key in self.angle_by_time.keys():
            if key in path:
                for unit in self.angle_by_time[key]['units']:
                    if unit in path:
                        recording_angle = self.angle_by_time[key]['angle']
        recordings_and_angles[i] = '\t'.join([path, recording_angle])


    f = open(parser.angles_txt_path,'w')
    f.write('\n'.join(recordings_and_angles))
    f.close()
        
if "__main__"==__name__:
    main()