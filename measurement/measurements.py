from __future__ import absolute_import, division, print_function, unicode_literals
from collections import OrderedDict

import numpy as np

from measurement.core import Measurement


class TimeOrderedStream(Measurement):
    """
    This class stores time-ordered data from a single channel.
    """

    _version = 0
    dimensions = OrderedDict([('time', ('time',)),
                              ('data', ('time',))])

    def __init__(self, time, data, state, description='TimeOrderedStream', validate=True):
        self.time = time
        self.data = data
        super(TimeOrderedStream, self).__init__(state=state, description=description, validate=validate)


class TimeOrderedStreamArray(Measurement):
    """
    This class stores time-ordered data from multiple, simultaneously-sampled channels.
    """

    _version = 0
    dimensions = OrderedDict([('time', ('time',)),
                              ('data', ('num_channels', 'time'))])

    def __init__(self, time, data, state, description='TimeOrderedStreamArray', validate=True):
        self.time = time
        self.data = data
        super(TimeOrderedStreamArray, self).__init__(state=state, description=description, validate=validate)

    @property
    def num_channels(self):
        return np.arange(self.data.shape[0])

    def __getitem__(self, number):
        tod = TimeOrderedStream(time=self.time, data=self.data[int(number), :], state=self.state,
                                description=self.description)
        tod._io = self._io
        tod._io_node_path = self._io_node_path
        return tod


class FrequencySweep(Measurement):
    """
    This class stores frequency-ordered data from a single channel.

    It can be used to store the result of a frequency sweep from a spectrum analyzer (in which case the `data` array is
    real) or from a vector network analyzer (in which case the `data` array is complex).
    """

    _version = 0
    dimensions = OrderedDict([('frequency', ('frequency',)),
                              ('data', ('frequency',))])

    def __init__(self, frequency, data, state, description='FrequencySweep', validate=True):
        self.frequency = frequency
        self.data = data
        super(FrequencySweep, self).__init__(state=state, description=description, validate=validate)


class SweepStream(Measurement):
    """
    This class stores a frequency sweep and a time-ordered data stream from a single channel.

    It can be used for time-ordered data from a superconducting resonator that is to be transformed into units of
    resonance frequency shift and dissipation shift.
    """

    _version = 0

    def __init__(self, sweep, stream, state=None, description="SweepStream", validate=True):
        self.sweep = sweep
        self.stream = stream
        super(SweepStream, self).__init__(state=state, description=description, validate=validate)
