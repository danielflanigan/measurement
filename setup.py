from setuptools import setup

setup(name="measurement",
      version="0.2.2",
      description="A library for reading and writing hierarchical scientific measurement data in multiple formats.",
      url="https://github.com/danielflanigan/measurement",
      author="Daniel Flanigan",
      author_email="daniel.isaiah.flanigan@gmail.com",
      license="MIT",
      packages=['measurement'],
      install_requires=[
            'numpy',
            'pandas'
      ],
      extras_require={
            'NetCDF4': 'netCDF4',
      },
      zip_safe=False)
