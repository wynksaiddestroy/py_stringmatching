============
Installation
============
This pages describes the requirements, dependencies and provides a step by step instruction
to install the py_stringmatching package.

Requirements
------------
    * Python 2.7 or Python 3.3+
    * C/C++ compiler

Platforms
------------
py_stringmatching has been tested on Linux, OSX and Windows.

Dependencies
------------
    * numpy>=1.7.0
    * six

.. note::

    The user need not install these dependency packages before installing the py_stringmatching package.
    The py_stringmatching installer will automatically install the required packages.

There are 2 ways to install py_stringmatching package - 1) installing from source distribution, or
(2) installing using pip.

Installing from source distribution
-------------------------------------
Step 1: Download the py_stringmatching package from `here
<https://testpypi.python.org/pypi/py_stringmatching/0.1.0>`_.

Step 2: Unzip the package and execute the following command from the package root::

    python setup.py install

This will install py_stringmatching package.

.. note::

    If the python package installation requires root permission then, you can install the package in
    your home directory like this::

        python setup.py install --user

    for more information look at the stackoverflow `link
    <http://stackoverflow.com/questions/14179941/how-to-install-python-packages-without-root-privileges>`_.

Installing using pip
--------------------
You can also install the package using pip::

    pip install py_stringmatching
 
