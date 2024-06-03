#!/usr/bin/env python

from distutils.core import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="vtkmat",
    version="1.0",
    description="Save content of vtk-file to .mat file for quick access.",
    author="Kai Steltner",
    license="MIT License",
    packages=["vtkmat"],
    install_requires=["PySide6>=6.7.0", "pyvista>=0.43.6", "scipy==1.13.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
)
