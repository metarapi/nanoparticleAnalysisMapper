# The package spcalext.c needs to be built.
# We're going to use the `build` command to build the package.

# Run this with the command:
# python build.py build_ext --inplace
# To build it for your own system.

from setuptools import Extension, setup, find_packages
import numpy as np

spcalext = Extension(
    "lib.spcalext",
    sources=["src/spcalext.c"],
    include_dirs=[np.get_include()],
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
)

setup(
    packages=find_packages(),
    ext_modules=[spcalext],
)