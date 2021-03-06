import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name ="box",
    version = "0.0.1",
    author = "Jose Luis Vallejo",
    author_email = "jvallejodiaz@gmail.com",
    description = ("Web framework base on werkzoug"),
    license = "BSD",
    keywords = "web framework",
    packages=['box', 'tests'],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
