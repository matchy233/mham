import json
import numpy as np
from scipy import interpolate

class Dataset:    
    # name: used for axis names
    # values: list of all sensor values in chronological order
    # timestamps: list of tuples (data_index, timestamp)
    def __init__(self, name, values, timestamps):
        self.title = name # Title for this collections of data
        self.values = values # list of numpy time series (for example [ax, ay az])
        self.raw_timestamps = timestamps # for plotting and processing, list of numpy array of timestamps for the axis
        self._update_values = None # all values with consecutive duplicate entries removed
        self._update_timestamps = None # timestamps for values with consecutive duplicate entries removed
        self._update_idxs = None # list idx for values with consecutive duplicate entries removed

        # calculate interpolated timestamps 
        # timestamps go linearly from first time to last time
        # seconds from start
        self._int_timestamps = None 

        # seconds between first and last sample
        self.total_time = (self.raw_timestamps[-1][1] - self.raw_timestamps[0][1]) / 1000
        # linearly interpolated offset in seconds from the first sample
        self.timestamps = np.linspace(0, self.total_time, num=len(values))
        
        # Calculate average sample rate
        # samples/s
        self.samplerate = len(self.values) / self.total_time 

        self._max_update_gap = None     
        
    #skip raw timestamp conversion
    #directly pass values and corresponding timestamps
    @classmethod
    def fromLists(cls, name, values, timestamps):
        raw_timestamps = [(n, 1000 * ts) for n, ts in zip(range(len(timestamps)), timestamps)]
        return cls(name, values, raw_timestamps)

    @property
    def update_timestamps(self):
        if self._update_timestamps is None:
            self._update_timestamps = [self.int_timestamps[idx] for idx in self.update_idxs]
        return self._update_timestamps

    @property
    def update_values(self):
        if self._update_values is None:
            self._update_values = [self.values[idx] for idx in self.update_idxs]
        return self._update_values

    @property
    def update_idxs(self):
        if self._update_idxs is None:
            vals = np.array(self.values, dtype=float)
            val_diffs = np.diff(vals, prepend=vals[0]-1)
            self._update_idxs = np.where(val_diffs > 0)[0]
        return self._update_idxs

    @property
    def max_update_gap(self):
        if self._max_update_gap is None:
            self._max_update_gap = max(np.diff(self.update_timestamps) / 1000) if len(self.update_timestamps) > 1 else np.inf
        return self._max_update_gap

    @property
    def int_timestamps(self):
        if self._int_timestamps is None:
            idxs = [rts[0] for rts in self.raw_timestamps]
            ts = [rts[1] for rts in self.raw_timestamps]

            self._int_timestamps = interpolate.interp1d(idxs, ts, fill_value="extrapolate")(np.arange(len(self.values)))
        return self._int_timestamps


    