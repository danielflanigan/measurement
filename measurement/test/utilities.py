"""
This module contains helper functions and data structures for running tests.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from measurement import core, measurements

bad_node_paths = ('', ' ', '"', ':', '\\', '?', '!', 'bad-hyphen', '0number', '//', '/bad/end/')
good_node_paths = ('/', 'relative', '/absolute', '/2/good', 'underscore_is_fine/_/__really__', '0/12/345')

corners = {'zero_int': 0,
           'zero_float': 0.,
           'one_int': 1,
           'one_float': 1.,
           'minus_one_int': -1,
           'minus_one_float': -1.,
           'two_int': 2,
           'two_float': 2.,
           'none': None,
           'true': True,
           'false': False,
           'empty_list': [],
           'int_list': [-1, 0, 1, 2],
           'float_list': [-0.1, 1, np.pi],
           'str_list': ['zero', 'one', 'two', ''],
           'bool_list': [False, True, False],
           'none_dict': {'none': None},
           'dict_dict': {'one': 1, 'a_dict': {'none': None, 'false': False, 'another_dict': {}}},
           'list_dict': {'empty_list': [],
                         'int_list': [-1, 0, 1, 2],
                         'float_list': [-0.1, 1, np.pi],
                         'str_list': ['zero', 'one', 'two', ''],
                         'bool_list': [False, True, False]}}


class CornerCases(core.Measurement):
    _version = 0

    def __init__(self,
                 zero_int=0,
                 zero_float=0.,
                 one_int=1,
                 one_float=1.,
                 minus_one_int=-1,
                 minus_one_float=-1.,
                 two_int=2,
                 two_float=2.,
                 none=None,
                 true=True,
                 false=False,
                 empty_list=[],
                 int_list=[-1, 0, 1, 2],
                 float_list=[-0.1, 1, np.pi],
                 str_list=['zero', 'one', 'two', ''],
                 bool_list=[False, True, False],
                 none_dict={'none': None},
                 dict_dict={'one': 1, 'a_dict': {'none': None, 'false': False, 'another_dict': {}}},
                 list_dict={'empty_list': [],
                            'int_list': [-1, 0, 1, 2],
                            'float_list': [-0.1, 1, np.pi],
                            'str_list': ['zero', 'one', 'two', ''],
                            'bool_list': [False, True, False]},
                 state=corners, description='CornerCases'):
        self.zero_int = zero_int
        self.zero_float = zero_float
        self.one_int = one_int
        self.one_float = one_float
        self.minus_one_int = minus_one_int
        self.minus_one_float = minus_one_float
        self.two_int = two_int
        self.two_float = two_float
        self.none = none
        self.true = true
        self.false = false
        self.empty_list = empty_list
        self.int_list = int_list
        self.float_list = float_list
        self.str_list = str_list
        self.bool_list = bool_list
        self.none_dict = none_dict
        self.dict_dict = dict_dict
        self.list_dict = list_dict
        super(CornerCases, self).__init__(state=state, description=description)


def fake_time_ordered_stream(num_samples=2 ** 10, length_seconds=0.01):
    time = np.linspace(0, length_seconds, num_samples)
    data = np.random.randn(num_samples) + 1j * np.random.randn(num_samples)
    state = core.StateDict(corners)
    description = "fake TimeOrderedStream"
    return measurements.TimeOrderedStream(time=time, data=data, state=state, description=description)


def fake_time_ordered_stream_array(num_channels=4, num_samples=2 ** 10, length_seconds=0.01):
    time = np.linspace(0, length_seconds, num_samples)
    data = np.random.randn(num_channels, num_samples) + 1j * np.random.randn(num_channels, num_samples)
    state = core.StateDict(corners)
    description = "fake TimeOrderedStreamArray"
    return measurements.TimeOrderedStreamArray(time=time, data=data, state=state, description=description)


def fake_frequency_sweep(num_frequencies=2 ** 10, start_frequency=1e9, stop_frequency=2e9):
    frequency = np.linspace(start_frequency, stop_frequency, num_frequencies)
    data = np.random.randn(num_frequencies) + 1j * np.random.randn(num_frequencies)
    state = core.StateDict(corners)
    description = "fake FrequencySweep"
    return measurements.FrequencySweep(frequency=frequency, data=data, state=state, description=description)


def fake_sweep_stream(num_frequencies=2 ** 10, start_frequency=1e9, stop_frequency=2e9, num_samples=2 ** 10,
                      length_seconds=0.01):
    sweep = fake_frequency_sweep(num_frequencies=num_frequencies, start_frequency=start_frequency,
                                 stop_frequency=stop_frequency)
    stream = fake_time_ordered_stream(num_samples=num_samples, length_seconds=length_seconds)
    state = core.StateDict(corners)
    description = "fake SweepStream"
    return measurements.SweepStream(sweep=sweep, stream=stream, state=state, description=description)
