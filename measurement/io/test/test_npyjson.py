from testfixtures import TempDirectory

from measurement.test import utilities
from measurement.io import npyjson


def test_read_write_measurement():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path)
        original = utilities.CornerCases()
        name = 'measurement'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_stream():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path)
        original = utilities.fake_time_ordered_stream()
        name = 'stream'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_streamarray():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path)
        original = utilities.fake_time_ordered_stream_array()
        name = 'stream_array'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_frequency_sweep():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path)
        original = utilities.fake_frequency_sweep()
        name = 'sweep'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_sweep_stream():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path)
        original = utilities.fake_sweep_stream()
        name = 'sweep_stream'
        io.write(original, name)
        assert original == io.read(name)


def test_memmap():
    with TempDirectory() as directory:
        io = npyjson.NpyJsonIO(directory.path, memmap=True)
        original = utilities.fake_time_ordered_stream()
        name = 'stream'
        io.write(original, name)
        assert original == io.read(name)
