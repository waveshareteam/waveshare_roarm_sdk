# encoding=utf-8
from __future__ import print_function
import sys

PYTHON_VERSION = sys.version_info[:2]
if PYTHON_VERSION != (2, 7) and PYTHON_VERSION < (3, 5):
    print("This roarm_sdk version requires Python 2.7, 3.5 or later.")
    sys.exit(1)

import setuptools
import textwrap
import roarm_sdk

install_requires = [
    "pyserial",
    "requests"
]

if sys.version_info >= (3, 10):
    install_requires.append("simplejson")

try:
    long_description = (
        open("README.md", encoding="utf-8").read()
        + open("docs/README.md", encoding="utf-8").read()
    )
except (FileNotFoundError, IOError):
    long_description = textwrap.dedent(
        """
        waveshare roarm sdk
        """
    )

setuptools.setup(
    name="roarm_sdk",
    version=roarm_sdk.__version__,
    author=roarm_sdk.__author__,
    author_email=roarm_sdk.__email__,
    description="waveshare roarm sdk.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=roarm_sdk.__git_url__,
    packages=setuptools.find_packages(),
    include_package_data=True,  # Include non-Python files, like JSON files
    package_data={"roarm_sdk": ["*.json"]},  # Specify the JSON file(s) to include
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)
