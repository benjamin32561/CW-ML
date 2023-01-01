import numpy as np

class Recording:
    def __init__(self,unit_id=0,recording_id=0,recording=[],class_dict=None):
        if class_dict==None:
            self.unit_id = unit_id
            self.recording_id = recording_id
            self.recording = recording
        else:
            for key in class_dict:
                setattr(self, key, class_dict[key])

class RecordingResponse:
    def __init__(self,unit_id,recording_id,model_output,recording_class):
        self.unit_id = unit_id
        self.recording_id = recording_id
        self.model_output = model_output
        self.recording_class = recording_class

class Request:
    def __init__(self,recordings,model_type,threshold=0.5):
        self.recordings = recordings
        self.model_type = model_type
        self.threshold = threshold

class Response:
    def __init__(self,recordings_output,status,error_msg=""):
        self.recordings_output = recordings_output
        self.status = status
        self.error_msg = error_msg

def RecordingsDictToClass(recordings_list):
    to_ret = []
    for recording_dict in recordings_list:
        to_ret.append(Recording(class_dict=recording_dict))
    return to_ret

def RecordingsClassToNumpy(recordings:list):
    to_ret = []
    for recording in recordings:
        to_ret.append(recording.recording)
    return np.array(to_ret).astype('float32')