import json
import numpy as np
import matplotlib.pyplot as plt
from .Dataset import Dataset


# data integrity check. Array values:
# [0]: 2: data required, 1: data desired, 0: data optional
# [1]: min mean f [Hz]
# [2]: max mean f [Hz]
# [3]: max update gap [s]
data_integrity = {
    'timestamp': [2, 10, 15, None],
    'packetNumber': [2, 10, 15, None],
    'lostPackets': [0, 0, 1, None],
    'note': [0, 0, 100, None],

    'ax': [2, 180, 220, 20],
    'ay': [2, 180, 220, 20],
    'az': [2, 180, 220, 20],
    'gx': [2, 180, 220, 20],
    'gy': [2, 180, 220, 20],
    'gz': [2, 180, 220, 20],
    'mx': [2, 10, 15, 30],
    'my': [2, 10, 15, 30],
    'mz': [2, 10, 15, 30],
    'temperature': [2, 10, 15, None],
    'longitude': [2, 0.5, 100, 120],
    'latitude': [2, 0.5, 100, 120],
    'altitude': [2, 0.5, 100, 120],
    'speed': [1, 0.5, 100, None],
    'bearing': [1, 0.5, 100, None],

    'phone_ax': [2, 20, 5000, 120],
    'phone_ay': [2, 20, 5000, 120],
    'phone_az': [2, 20, 5000, 120],
    'phone_gx': [2, 20, 5000, 120],
    'phone_gy': [2, 20, 5000, 120],
    'phone_gz': [2, 20, 5000, 120],
    'phone_mx': [2, 1, 500, 120],
    'phone_my': [2, 1, 500, 120],
    'phone_mz': [2, 1, 500, 120],

    'phone_gravx': [1, 10, 1000, None],
    'phone_gravy': [1, 10, 1000, None],
    'phone_gravz': [1, 10, 1000, None],
    'phone_lax': [1, 10, 1000, None],
    'phone_lay': [1, 10, 1000, None],
    'phone_laz': [1, 10, 1000, None],
    'phone_rotx': [1, 10, 1000, None],
    'phone_roty': [1, 10, 1000, None],
    'phone_rotz': [1, 10, 1000, None],
    'phone_rotm': [1, 10, 1000, None],
    'phone_magrotx': [0, 5, 1000, None],
    'phone_magroty': [0, 5, 1000, None],
    'phone_magrotz': [0, 5, 1000, None],
    'phone_orientationx': [1, 10, 1000, None],
    'phone_orientationy': [1, 10, 1000, None],
    'phone_orientationz': [1, 10, 1000, None],
    'phone_light': [0, 0.1, 50, None],
    'phone_steps': [0, 0.1, 50, None],
    'phone_temp': [0, 0.1, 50, None],
    'phone_pressure': [1, 0.1, 50, None],
    'phone_humidity': [0, 0.1, 50, None],
}


class Recording:
    def __init__(self, filename, no_labels=True, mute=True):
        self.data = {} # Dictionary that holds datasets
        self.raw_data = None # Will hold a dictionary directly read from the JSON file
        self.labels = None
        self.readFile(filename, no_labels, mute)
        self.getAllData()

    def getData(self, key):
        raw_timestamps = [] # List of tuples (data_index, timestamp)
        raw_values = []
        for packet in self.raw_data:
            timestamp = packet['timestamp']
            raw_timestamps.append((len(raw_values), timestamp))
            if key in packet and isinstance(packet[key], str): # this is for notes
                raw_values.append(packet[key])
            elif key in packet and hasattr(packet[key], "__len__"):
                raw_values.extend(packet[key])
            elif key in packet and not hasattr(packet[key], "__len__"):
                raw_values.append(packet[key])

        dataset = Dataset(key, raw_values, raw_timestamps)
        dataset.title = key
        
        self.data[key] = dataset
        
    def getAllData(self):
        keys = set()
        for packet in self.raw_data:
            keys.update(list(packet.keys()))
            
        for key in keys:
            self.getData(key)
            

    def readFile(self, filename, no_labels, mute):
        with open(filename, 'r') as file:
            file_str = file.read()
            # Terminates JSON array if app crashed before finish writing the file
            if file_str[0] == '[' and file_str[-1] != ']':
                file_str += ']'
            self.raw_data = json.loads(file_str) 

        if not(isinstance(self.raw_data, list)):
            self.labels = self.raw_data['labels']
            self.raw_data = self.raw_data['data']
            if not(mute):
                print("Loaded data from file that also contains labels. Access them using [varname].labels")
                print("Please mute this message by setting mute=True in your algorithm submission")
        else:
            if no_labels:
                if not(mute):
                    print("Loaded data from file that does not contain labels.")
                    print("Please mute this message by setting mute=True in your algorithm submission")
            else:
                self.addLabels(filename)

    def addLabels(self, filename):
        self.labels = {}
        inp = ""
        while inp != "y":
            print("New data file without labels, please provide labels, if you want to later upload it for submission or label it for internal use!")
            print("Note: Please deactivate this function by setting no_labels=True in your algorithm submission")
            while inp != "n":
                print("\r\n\nWhere was the board worn? (0 - wrist left, 1 - belt, 2 - right ankle), provide either an integer (e.g. '0') or a string (e.g.'wrist left'), n: cancel")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    elif len(inp) == 1 and int(inp)<3 and int(inp) >= 0:
                        self.labels["board_loc"] = int(inp)
                    elif inp in ["wrist left", "wrist"]:
                        self.labels["board_loc"] = 0
                    elif inp in ["belt"]:
                        self.labels["board_loc"] = 1
                    elif inp in ["right ankle", "ankle"]:
                        self.labels["board_loc"] = 2
                    else:
                        raise ValueError()
                    break
                except:
                    print("Error: Input not recognized, try again!")

            while inp != "n":
                print("\r\n\nWhat path was this trace recorded on? Provide integer in [0, 4] corresponding to the path index in the task set (e.g. '0'), n: cancel")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    elif len(inp) == 1 and int(inp)<5 and int(inp) >= 0:
                        self.labels["path_idx"] = int(inp)
                    else:
                        raise ValueError()
                    break
                except:
                    print("Error: Input not recognized, try again!")


            while inp != "n":
                print("\r\n\nWhat activities are included in the trace (min. 1 min, See task set for specifications)?")
                print("0: standing still, 1: walk, 2: run, 3: cycle")
                print("Provide integer comma separated list of integers or strings, avoid duplicates (input e.g., '0, 2' or 'standing still, run'), n: cancel")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    else:
                        self.labels["activities"] = []
                        inputs = inp.replace(" ", "").split(",")
                        for val in inputs:
                            if val in ["0", "standing still", "standing"]:
                                self.labels["activities"].append(0)
                            elif val in ["1", "walk", "walking"]:
                                self.labels["activities"].append(1)
                            elif val in ["2", "run", "running"]:
                                self.labels["activities"].append(2)
                            elif val in ["3", "cycle", "cycling", "bicycle"]:
                                self.labels["activities"].append(3)
                            elif val in ["4", "tram ride", "tram"]:
                                self.labels["activities"].append(4)
                            elif val in ["5", "polybahn ride", "polybahn"]:
                                self.labels["activities"].append(5)
                            else:
                                raise ValueError()
                    break
                except:
                    self.labels["activities"] = []
                    print("Error: Input not recognized, try again!")

            while inp != "n":
                print("\r\n\nWhat is the birth sex of the person who recorded the data?")
                print("f - female, m - male, s - prefer not to respond")
                print("(This data is acquired to improve the data set quality for possible further analysis)")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    elif inp in ["f", "female", "F", "Female"]:
                        self.labels["gender"] = "f"
                    elif inp in ["m", "male", "M", "Male"]:
                        self.labels["gender"] = "m"
                    elif inp in ["s", "S"]:
                        self.labels["gender"] = "n/a"
                    else:
                        raise ValueError()
                    break
                except:
                    print("Error: Input not recognized, try again!")

            while inp != "n":
                print("\r\n\nWhat is the body height of the person who recorded the data?")
                print("Answer with an integer representing centimeters: e.g., 172")
                print("(This data is acquired to improve the data set quality for possible further analysis)")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    elif len(inp) == 3 and int(inp)<240 and int(inp) >= 130:
                        self.labels["body_height"] = int(inp)
                    else:
                        raise ValueError()
                    break
                except:
                    print("Error: Input not recognized, try again!")

            while inp != "n":
                print("\r\n\nWhat is the legi number of the person who recorded the data?")
                print("Answer with a string: e.g., 01-234-567")
                print("(This data is not published but used for verification and to avoid wrongfully assigning data to a group)")
                inp = input()
                try:
                    if inp == "n":
                        print("Cancel, continue without labels. This can be automated by passing the no_labels=True argument to this function")
                        self.labels = None
                        return
                    elif len(inp) == 10:
                        self.labels["legi"] = inp
                    else:
                        raise ValueError()
                    break
                except:
                    print("Error: Input not recognized, try again!")

            print("\r\n\nPlease re-check and confirm that the following labels are correct: (y - confirm, n - redo)")
            print(self.labels)
            inp = input()
        
        print("Saving file...")
        new_data = {'labels': self.labels, 'data': self.raw_data}

        # Change output directory if working on Kaggle as data cannot be saved to the input folder on Kaggle
        if 'kaggle' in filename:
            filename = '/kaggle/working/' + filename.split('/')[-1]

        with open(filename, 'w') as f:
            json.dump(new_data, f, indent=1)
        print("This file is now ready for submission: {}".format(filename))

    # keys in form ['ax', 'ay', 'az'] -> plots ax,ay,az in same plot
    # or keys in the form [['ax', 'ay', 'az'], ['gx', 'gy', 'gz']] -> two subplots
    # ylables in the form ['Accelerometer', 'Gyroscope']
    # labels in the same structure like keys [['acc_x', 'acc_x', 'acc_z'], ['gyro_x', 'gyro_y', 'gyro_z']]
    def plot(self, keys, ylabels=None, labels=None):
        #check if keys are two dimensional
        if not isinstance(keys[0], list): keys = [keys]
        if labels is not None and not isinstance(labels[0], list): labels = [labels]
        
        fig,ax=plt.subplots(nrows=len(keys),ncols=1,figsize=(10, 6), sharex=True, squeeze=False)

        for i, key_group in enumerate(keys):
            if ylabels is not None:
                ax[i][0].set_ylabel(ylabels[i])
                
            for j, key in enumerate(key_group):
                label = labels[i][j] if labels is not None else self.data[key].title
                ax[i][0].plot(self.data[key].timestamps, self.data[key].values, label=label)
                
            ax[i][0].legend(loc='lower right')
            ax[i][0].grid()
                
        ax[-1][0].set_xlabel('Time[s]')

        plt.show()

    def checkDataIntegrity(self, mute=False):
        str_output = []
        err_cnt = 0
        warn_cnt = 0
        for key in data_integrity:
            if key in self.data:
                if self.data[key].samplerate < data_integrity[key][1] or self.data[key].samplerate > data_integrity[key][2]:
                    if data_integrity[key][0] == 2:
                        print_str = "\U0001f534 Error: Required data trace {}\t|| unexpected sampling rate {:.2f}Hz (expected interval: [{:.2f}, {:.2f}]Hz)".format(key, self.data[key].samplerate, data_integrity[key][1], data_integrity[key][2])
                        str_output.append(print_str)
                        if not mute:
                            print(print_str)
                        err_cnt += 1
                    elif data_integrity[key][0] == 1:
                        print_str = "\U0001f7e0 Warning: Non-essential data trace {}\t|| unexpected sampling rate {:.2f}Hz (expected interval: [{:.2f}, {:.2f}]Hz)".format(key, self.data[key].samplerate, data_integrity[key][1], data_integrity[key][2])
                        str_output.append(print_str)
                        if not mute:
                            print(print_str)
                        warn_cnt += 1

                elif data_integrity[key][3] is not None and self.data[key].max_update_gap > data_integrity[key][3]:
                    if data_integrity[key][0] == 2:
                        print_str = "\U0001f534 Error: Required data trace {}\t|| max update gap exceeded {:.2f}s (max update gap: {:.2f}s)".format(key, self.data[key].max_update_gap, data_integrity[key][3])
                        str_output.append(print_str)
                        if not mute:
                            print(print_str)
                        err_cnt += 1
                    elif data_integrity[key][0] == 1:
                        print_str = "\U0001f7e0 Warning: Non-essential data trace {}\t|| max update gap exceeded {:.2f}s (max update gap: {:.2f}s)".format(key, self.data[key].max_update_gap, data_integrity[key][3])
                        str_output.append(print_str)
                        if not mute:
                            print(print_str)
                        warn_cnt += 1

            else:
                if data_integrity[key][0] == 2:
                    print_str = "\U0001f534 Error: Required data trace {} missing".format(key)
                    str_output.append(print_str)
                    if not mute:
                        print(print_str)
                    err_cnt += 1
                elif data_integrity[key][0] == 1:
                    print_str = "\U0001f7e0 Warning: data trace {} missing".format(key)
                    str_output.append(print_str)
                    if not mute:
                        print(print_str)
                    warn_cnt += 1

        if 'ax' in self.data:
            t = (self.data['ax'].raw_timestamps[-1][1]-self.data['ax'].raw_timestamps[0][1])//1000
            if t > 3600:
                print_str = "\U0001f534 Error: Trace is unexpectedly long ({:.2f} seconds). May be ok for training but not for submission".format(t)
                str_output.append(print_str)
                if not mute:
                    print(print_str)
                err_cnt += 1
            if t < 120:
                print_str = "\U0001f534 Error: Trace is unexpectedly short ({:.2f} seconds). May be ok for training but not for submission".format(t)
                str_output.append(print_str)
                if not mute:
                    print(print_str)
                err_cnt += 1
        
        if not mute:
            print("Finished Integrity Check!")
            if err_cnt > 0:
                print("\U0001f534 Due to the errors above, the trace is not suitable for submission")
            elif warn_cnt > 15:
                print("\U0001f534 More than 15 non-essential data traces are missing, therefore, the trace is not suitable for submission")
                print("Please check the phone permission settings")
            elif warn_cnt > 0:
                print("\U0001f7e0 Despite missing {} non-essential sensors, this trace is suitable for submission as far as this automated test can judge.".format(warn_cnt))
            else:
                print("\u2705 All good. As far as this test can judge, the data is valid for submission")

        if self.labels is None or len(self.labels.keys()) == 0:
            print_str = "\U0001f7e0 However, the trace is missing the required labels for submission"
            str_output.append(print_str)
            if not mute:
                print(print_str)
            missing_labels = True
        else:
            missing_labels = False

        return err_cnt, warn_cnt, missing_labels, str_output 

    def DataIntegrityCheck(self, mute=False):
        return self.checkDataIntegrity(mute=mute)
