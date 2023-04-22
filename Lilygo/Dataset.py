import json
import numpy as np
from scipy import interpolate

class Dataset:
    """
    A class representing a collection of sensor readings.

    Attributes:
        title (str): Title for this collection of data.
        values (list): List of corresponding sensor values in chronological order.
        raw_timestamps (list): List of tuples (data_index, timestamp) written for every packet, also if no data for this collection was added; data_index may be repeated (last entry counts); timestamp in milliseconds.
        total_time (float): Time in seconds between start and end of recording (i.e., length of recording).
        timestamps (numpy.ndarray): Timestamp offset for each sensor value (since start of recording in seconds) obtained by linearly interpolating between the start and end of the recording, interpolates also over sampling gaps (i.e., timestamps are potentially inaccurate in case a sensor fails to report values for longer periods of time).
        samplerate (float): Mean sample rate over the whole duration of the recording in samples/s.
        _update_timestamps (list): Timestamps for values with consecutive duplicate entries removed.
        _update_values (list): Sensor values with consecutive duplicate entries removed.
        _update_idxs (list): List indices for values with consecutive duplicate entries removed.
        _max_update_gap (float): Maximum duration in seconds for which the sensor value does not change.
        _int_timestamps (numpy.ndarray): Interpolated timestamp offset for each sensor value (since start of recording in seconds) obtained by interpolating between raw timestamps, should be correct also in case a sensor stops reporting values over a segment of the recording but individual sampling intervals might vary.

    Methods:
        fromLists(cls, name, values, timestamps): Create a new Dataset object from the given name, values, and timestamp offsets.
        update_timestamps(self): Get the update timestamps.
        update_values(self): Get the update values.
        update_idxs(self): Get the update indices.
        max_update_gap(self): Get the maximum update gap.
        int_timestamps(self): Get the interpolated timestamps.

    """

    def __init__(self, name, values, timestamps):
        self.title = name
        self.values = values
        self.raw_timestamps = timestamps
        self.total_time = (self.raw_timestamps[-1][1] - self.raw_timestamps[0][1]) / 1000 
        self.timestamps = np.linspace(0, self.total_time, num=len(values))
        self.samplerate = len(self.values) / self.total_time
        self._update_timestamps = None
        self._update_values = None
        self._update_idxs = None
        self._max_update_gap = None
        self._int_timestamps = None
        

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
            self._update_idxs = np.where(val_diffs != 0)[0].tolist()
        return self._update_idxs

    @property
    def max_update_gap(self):
        if self._max_update_gap is None:
            timestamps = self.update_timestamps.copy()
            if self.update_timestamps[0] > 0: # if first sensor value was captured after start of recording
                timestamps = [0,] + timestamps
            if self.update_timestamps[-1] < self.total_time: # if last sensor update happened before end of recording
                timestamps.append(self.total_time)
            self._max_update_gap = max(np.diff(timestamps)) if len(timestamps) > 1 else np.inf
        return self._max_update_gap

    @property
    def int_timestamps(self):
        if self._int_timestamps is None:
            idxs = []
            ts = []
            assert len(self.raw_timestamps)>1
            for rts, next_rts in zip(self.raw_timestamps[:-1], self.raw_timestamps[1:]):
                if rts[0] != next_rts[0]:
                    idxs.append(rts[0])
                    ts.append(rts[1])

            if len(self.values)>self.raw_timestamps[-1][0]:
                idxs.append(self.raw_timestamps[-1][0])
                ts.append(self.raw_timestamps[-1][1])

            self._int_timestamps = (interpolate.interp1d(idxs, ts, fill_value="extrapolate")(np.arange(len(self.values))) - self.raw_timestamps[0][1]) / 1000
        return self._int_timestamps
