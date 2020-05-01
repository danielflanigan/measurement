import os

from testfixtures import TempDirectory

from measurement.test import utilities
from measurement.io import netcdf


def test_read_write_measurement():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = netcdf.NetcdfIO(os.path.join(directory.path, filename))
        original = utilities.CornerCases()
        name = 'measurement'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_time_ordered_stream():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = netcdf.NetcdfIO(os.path.join(directory.path, filename))
        original = utilities.fake_time_ordered_stream()
        name = 'stream'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_time_ordered_stream_array():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = netcdf.NetcdfIO(os.path.join(directory.path, filename))
        original = utilities.fake_time_ordered_stream()
        name = 'stream_array'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_frequency_sweep():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = netcdf.NetcdfIO(os.path.join(directory.path, filename))
        original = utilities.fake_frequency_sweep()
        name = 'sweep'
        io.write(original, name)
        assert original == io.read(name)


def test_read_write_sweep_stream():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = netcdf.NetcdfIO(os.path.join(directory.path, filename))
        original = utilities.fake_sweep_stream()
        name = 'sweep_stream'
        io.write(original, name)
        assert original == io.read(name)


# ToDo: update caching code
"""
def test_cached_single_stream():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = nc.NCFile(os.path.join(directory.path, filename), cache_s21_raw=True)
        original = utilities.fake_single_stream()
        name = 'measurement'
        io.write(original, name)
        assert np.all(original.s21_raw == io.read(name).s21_raw)


def test_cached_stream_array():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = nc.NCFile(os.path.join(directory.path, filename), cache_s21_raw=True)
        original = utilities.fake_stream_array()
        name = 'measurement'
        io.write(original, name)
        assert np.all(original.s21_raw == io.read(name).s21_raw)


# TODO: implement me!

def test_from_series():
    with TempDirectory() as directory:
        filename = 'test.nc'
        io = nc.NCFile(os.path.join(directory.path, filename))
        original = utilities.CornerCases()
        name = 'corner_cases'
        io.write(original, name)
        io.close()
        df = original.to_dataframe()
        original.add_origin(df)
        assert original == core.from_series(df.iloc[0])
"""
