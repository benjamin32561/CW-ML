import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from os import makedirs
from os.path import join, exists

XLSX_RELEVENT_COLUMNS = ["X axis (G)","Y axis (G)","Z axis (G)","Time (sec)"]

AVG_LABEL = "AVG Force"
AVG_MAX_LABEL = "AVG Max Force Time"
X_MAX_LABEL = "X Max Force Time"
Y_MAX_LABEL = "Y Max Force Time"
Z_MAX_LABEL = "Z Max Force Time"
MAX_PULSE_LABEL = "Max Pulse Range"

X_AXIS_LABEL = "Time (sec)"
Y_AXIS_LABEL = "Force (G)"

X_COLOR = '#0000ff'
Y_COLOR = '#00ff00'
Z_COLOR = '#ff0000'
AVG_COLOR = '#7e9bc1'
PULSE_WIDTH_COLOR = "#000000"

FORCE_LINESTYLE = '-'
MAX_FORCE_LINESTYLE = '--'
MAX_PULSE_LINESTYLE = ':'

RECORD_TIME = 3.38
FREQUENCY = 200
MAIN_PULSE_START_END = 0.02

def CreatePath(path=str):
    if not exists(path):
        makedirs(path)

def GetAllXlsxInFolders(folders,folders_class):
    all_xlsx_with_class = []
    for idx, folder in enumerate(folders):
        xlsx_in_folder = glob(join(folder,'*.xlsx'))
        lines = [xlsx_loc+'\t'+folders_class[idx] for xlsx_loc in xlsx_in_folder]
        all_xlsx_with_class.extend(lines)
    return all_xlsx_with_class

def SaveLinesToTxt(lines,txt_filename='lines.txt'):
    to_write = '\n'.join(lines)
    with open(txt_filename,'w+') as f:
        f.write(to_write)

def CalcFrequency(df:pd.DataFrame()):
    return (df.shape[0]-1)/df.iloc[-1][-1]

def GetDataFrame(xlsx_path:str):
    data = pd.read_xlsx(xlsx_path)

    cols_to_drop = []
    for col in current_cols:
        if col not in XLSX_RELEVENT_COLUMNS:
            cols_to_drop.append(col)

    data = data.drop(cols_to_drop,axis=1)
    return data

def GetAbsMaxIdx(arr:np.ndarray):
    return np.argmax(np.absolute(arr))

def GetAbsMaxIdxByCol(df:pd.DataFrame,col:str):
    return GetAbsMaxIdx(df[col].to_numpy())

def GetMaxPulseRange(x:np.ndarray,max_idx:int):
    start = 0
    end = max_idx
    i = 0
    while i<max_idx:
        if np.absolute(x[i])<MAIN_PULSE_START_END:
          start=i
        i+=1
    while i<x.shape[0]:
        if np.absolute(x[i])<MAIN_PULSE_START_END:
            end=i
            break
        i+=1
    return start,end

def PlotRecordData(df:pd.DataFrame,plot_max=True,plot_pulse=True,print_info=True,save_to='',show_plot=True):
    cols = df.columns

    #plot graphs
    x = df[cols[0]].to_numpy()
    y = df[cols[1]].to_numpy()
    z = df[cols[2]].to_numpy()
    time = df[cols[3]].to_numpy()
    avg = np.mean(np.abs(np.array([x,y,z])),axis=0)
    plt.plot(time,x, label=cols[0],color=X_COLOR,linestyle=FORCE_LINESTYLE)
    plt.plot(time,y, label=cols[1],color=Y_COLOR,linestyle=FORCE_LINESTYLE)
    plt.plot(time,z, label=cols[2],color=Z_COLOR,linestyle=FORCE_LINESTYLE)
    plt.plot(time,avg, label=AVG_LABEL,color=AVG_COLOR,linestyle=FORCE_LINESTYLE)
    plt.xlabel(X_AXIS_LABEL)
    plt.ylabel(Y_AXIS_LABEL)

    #plot max's
    avg_max_idx = GetAbsMaxIdx(avg)
    if plot_max:
        x_max_idx = GetAbsMaxIdxByCol(df,cols[0])
        y_max_idx = GetAbsMaxIdxByCol(df,cols[1])
        z_max_idx = GetAbsMaxIdxByCol(df,cols[2])
        plt.axvline(time[x_max_idx],color=X_COLOR,label=X_MAX_LABEL,linestyle=MAX_FORCE_LINESTYLE)
        plt.axvline(time[y_max_idx],color=Y_COLOR,label=Y_MAX_LABEL,linestyle=MAX_FORCE_LINESTYLE)
        plt.axvline(time[z_max_idx],color=Z_COLOR,label=Z_MAX_LABEL,linestyle=MAX_FORCE_LINESTYLE)
        plt.axvline(time[avg_max_idx],color=AVG_COLOR,label=AVG_MAX_LABEL,linestyle=MAX_FORCE_LINESTYLE)

    #plot pulse width
    if plot_pulse:
        avg_pulse_start, avg_pulse_end = GetMaxPulseRange(avg,avg_max_idx)
        plt.axvline(time[avg_pulse_start],color=PULSE_WIDTH_COLOR,label=MAX_PULSE_LABEL,linestyle=MAX_PULSE_LINESTYLE)
        plt.axvline(time[avg_pulse_end],color=PULSE_WIDTH_COLOR,label=MAX_PULSE_LABEL,linestyle=MAX_PULSE_LINESTYLE)

    if print_info:
        #avg pulse integral
        print("AVG Force Work: ",np.sum(np.abs(avg[avg_pulse_start:avg_pulse_end])))
        #angle of accident
        print("Angle of accident (tan(x/y)): ", np.tan(y[avg_max_idx]/x[avg_max_idx]))

    plt.legend(loc='best')
    if save_to!='':
        plt.savefig(save_to)
    if show_plot:
        plt.show()
    plt.close()