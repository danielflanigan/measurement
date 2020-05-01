from __future__ import absolute_import, division, print_function, unicode_literals
import copy
import numpy as np

from measurement import core, measurements
from measurement.io import dictionary
from measurement.test import utilities


def test_measurement_instantiation_blank():
    m = core.Measurement()
    assert m.state == core.StateDict()
    assert m.description == ''
    assert m._parent is None
    assert m._io is None
    assert m._io_node_path is None


def test_node_composite_add_origin():
    original = utilities.fake_sweep_stream()
    io = dictionary.Dictionary()
    name = 'sweep_stream'
    io.write(original, name)
    ss = io.read(name)
    ss_df = ss.to_dataframe(add_origin=True)
    for k, row in ss_df.iterrows():
        assert row.io_class == 'Dictionary'
        assert row.root_path is None
        assert row.node_path == core.join('/', name)
    sweep = io.read(core.join(name, 'sweep'))
    stream = io.read(core.join(name, 'stream'))
    composite = measurements.SweepStream(sweep=sweep, stream=stream)
    composite_df = composite.to_dataframe(add_origin=True)
    for k, row in composite_df.iterrows():
        assert row.io_class is None
        assert row.root_path is None
        assert row.node_path is None
        assert row['sweep.io_class'] == 'Dictionary'
        assert row['sweep.root_path'] is None
        assert row['sweep.node_path'] == core.join('/', name, 'sweep')
        assert row['stream.io_class'] == 'Dictionary'
        assert row['stream.root_path'] is None
        assert row['stream.node_path'] == core.join('/', name, 'stream')


def test_measurement_list():
    length = 3
    contents = [utilities.CornerCases() for _ in range(length)]
    ml = core.MeasurementList(contents)
    assert len(ml) == length
    assert np.all(ml == contents)
    assert np.all(m._parent is ml for m in ml)


# ToDo: replace with single point
"""
def test_io_list():
    num_streams = 3
    streams = core.MeasurementList([utilities.CornerCases() for n in range(num_streams)])
    io = dictionary.Dictionary()
    sweep = measurements.FrequencySweep(core.IOList())
    io.write(sweep)
    sweep.streams.extend(streams)
    assert io.read(io.node_names()[0]) == measurements.FrequencySweep(streams)
"""


# ToDo: flesh out
def test_state_dict():
    s = core.StateDict()
    s = core.StateDict({})
    s.copy()


def test_read_write():
    io = dictionary.Dictionary()
    original = utilities.CornerCases()
    name = 'test'
    io.write(original, name)
    assert original == io.read(name)


def test_eq_state():
    m1 = utilities.CornerCases()
    m2 = utilities.CornerCases()
    assert m1 == m2
    m1.state['test'] = 1
    m2.state['test'] = 2
    assert m1 != m2


def test_eq_array():
    m1 = utilities.fake_time_ordered_stream()
    m2 = measurements.TimeOrderedStream(**dict([(k, copy.copy(v)) for k, v in m1.__dict__.items()
                                                if not k.startswith('_')]))
    assert m1 == m2
    index = np.random.random_integers(0, m1.data.size)
    m2.data[index] += 1
    assert m1 != m2
    m1.data[index] = m2.data[index] = np.nan
    assert m1 == m2


def test_comparison_code_attribute():
    m1 = utilities.CornerCases()
    m2 = utilities.CornerCases()
    m1.attribute = 1
    m2.attribute = 2
    assert m1 != m2


def test_join():
    assert core.join('one') == 'one'
    assert core.join('one', 'two', 'three') == 'one/two/three'
    assert core.join('/one', '/two', '/three') == '/three'


def test_split():
    assert core.split('') == ('', '')
    assert core.split('one') == ('', 'one')
    assert core.split('/one') == ('/', 'one')
    assert core.split('one/two/three') == ('one/two', 'three')
    assert core.split('/one/two/three') == ('/one/two', 'three')


def test_explode():
    assert core.explode('/') == []
    assert core.explode('boom') == ['boom']
    assert core.explode('/boom') == ['boom']
    assert core.explode('boom/kaboom') == ['boom', 'kaboom']


def test_validate_node_path():
    for bad in utilities.bad_node_paths:
        try:
            core.validate_node_path(bad)
            raise AssertionError("Invalid path {} should have failed".format(bad))
        except core.MeasurementError:
            pass
    for good in utilities.good_node_paths:
        try:
            core.validate_node_path(good)
        except core.MeasurementError:
            raise AssertionError("Valid path {} should not have failed.".format(good))


"""
def test_sweep_stream_array_node_path():
    original = utilities.fake_sweep_stream_array()
    # The current node path reflects the existing structure, while the IO node path is None until a read or write.
    assert original.current_node_path == '/'
    assert original.io_node_path is None
    assert original.sweep_array.current_node_path == '/sweep_array'
    assert original.sweep_array.io_node_path is None
    assert original.sweep_array.stream_arrays.current_node_path == '/sweep_array/stream_arrays'
    assert original.sweep_array.stream_arrays.io_node_path is None
    assert original.sweep_array.stream_arrays[0].current_node_path == '/sweep_array/stream_arrays/0'
    assert original.sweep_array.stream_arrays[0].io_node_path is None
    # Write the tree to disk.
    io = dictionary.Dictionary()
    name = 'ssa'
    io.write(original, name)
    # The current node path is unchanged, while the IO node path reflects how it has been stored to disk.
    assert original.current_node_path == '/'
    assert original.io_node_path == '/ssa'
    assert original.sweep_array.current_node_path == '/sweep_array'
    assert original.sweep_array.io_node_path == '/ssa/sweep_array'
    assert original.sweep_array.stream_arrays.current_node_path == '/sweep_array/stream_arrays'
    assert original.sweep_array.stream_arrays.io_node_path == '/ssa/sweep_array/stream_arrays'
    assert original.sweep_array.stream_arrays[0].current_node_path == '/sweep_array/stream_arrays/0'
    assert original.sweep_array.stream_arrays[0].io_node_path == '/ssa/sweep_array/stream_arrays/0'
    # The IO node path should be the same regardless of how much of the tree was loaded, while the current node path
    # depends on the actual measurement structure that exists.
    ssa = io.read(name)
    assert ssa.current_node_path == '/'
    assert ssa._io_node_path == '/ssa'
    assert ssa.sweep_array.current_node_path == '/sweep_array'
    assert ssa.sweep_array.io_node_path == '/ssa/sweep_array'
    assert ssa.sweep_array.stream_arrays.current_node_path == '/sweep_array/stream_arrays'
    assert ssa.sweep_array.stream_arrays.io_node_path == '/ssa/sweep_array/stream_arrays'
    assert ssa.sweep_array.stream_arrays[0].current_node_path == '/sweep_array/stream_arrays/0'
    assert ssa.sweep_array.stream_arrays[0].io_node_path == '/ssa/sweep_array/stream_arrays/0'
    sweep_array = io.read(core.join(name, 'sweep_array'))
    assert sweep_array.current_node_path == '/'
    assert sweep_array._io_node_path == '/ssa/sweep_array'
    assert sweep_array.stream_arrays.current_node_path == '/stream_arrays'
    assert sweep_array.stream_arrays.io_node_path == '/ssa/sweep_array/stream_arrays'
    assert sweep_array.stream_arrays[0].current_node_path == '/stream_arrays/0'
    assert sweep_array.stream_arrays[0].io_node_path == '/ssa/sweep_array/stream_arrays/0'
    stream_arrays = io.read(core.join(name, 'sweep_array', 'stream_arrays'))
    assert stream_arrays.current_node_path == '/'
    assert stream_arrays._io_node_path == '/ssa/sweep_array/stream_arrays'
    assert stream_arrays[0].current_node_path == '/0'
    assert stream_arrays[0].io_node_path == '/ssa/sweep_array/stream_arrays/0'
    stream_array_0 = io.read(core.join(name, 'sweep_array', 'stream_arrays', '0'))
    assert stream_array_0.current_node_path == '/'
    assert stream_array_0._io_node_path == '/ssa/sweep_array/stream_arrays/0'
    # Add the tree to a new measurement:
    m = core.Measurement()
    moved = ssa.sweep_array
    m.moved = moved
    # The IO node path is unchanged, while the current node path now reflects that the sweep array was last added to
    # the new measurement with the name 'moved'.
    assert ssa.current_node_path == '/'
    assert ssa._io_node_path == '/ssa'
    assert moved.current_node_path == '/moved'
    assert moved.io_node_path == '/ssa/sweep_array'
    assert moved.stream_arrays.current_node_path == '/moved/stream_arrays'
    assert moved.stream_arrays.io_node_path == '/ssa/sweep_array/stream_arrays'
    assert moved.stream_arrays[0].current_node_path == '/moved/stream_arrays/0'
    assert moved.stream_arrays[0].io_node_path == '/ssa/sweep_array/stream_arrays/0'
"""
