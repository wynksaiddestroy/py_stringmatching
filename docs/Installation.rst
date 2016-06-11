============
Installation
============
 
Requirements
------------
    * Python 2.7 or Python 3.3+
    * C/C++ compiler

Platforms
------------
py_stringmatching has been tested on Linux (Ubuntu with  Kernel Version 3.13.0-40-generic), OS X (Darwin with Kernel Version: 13.4.0), and Windows 8.1.

Dependencies
------------
    * numpy 1.7.0 or higher
    * six

.. note::

    The user does not have to install these dependency packages before installing the py_stringmatching package.
    The py_stringmatching installer will automatically install the required packages.

There are two ways to install py_stringmatching package: from source distribution or using pip.

Installing From Source Distribution
-------------------------------------
Step 1: Download the py_stringmatching package from `here
<https://testpypi.python.org/pypi/py_stringmatching/0.1.0>`_.

Step 2: Unzip the package and execute the following command from the package root to install the package::

    python setup.py install
    
.. note::

    If the Python package installation requires root permission then you can install the package in
    your home directory as follows::

        python setup.py install --user

    For more information see the StackOverflow `link
    <http://stackoverflow.com/questions/14179941/how-to-install-python-packages-without-root-privileges>`_.

Installing Using pip
--------------------
You can also install the package using pip::

    pip install py_stringmatching
