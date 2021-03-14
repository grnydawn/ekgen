===============
Getting-started
===============



-------------
Installation
-------------

The easiest way to install ekgen is to use pip python package manager. 

        >>> pip install ekgen

You can install ekgen from github code repository if you want to try the latest version.

        >>> git clone https://github.com/grnydawn/ekgen.git - Connect to preview 
        >>> cd ekgen
        >>> python setup.py install

Once installed, you can test the installation by running following command.

        >>> ekgen --version
        ekgen 0.1.0

------------
Requirements
------------

- Linux OS
- Python 3.5+ or PYthon 2.7
- Make building tool(make)
- C Preprocessor(cpp)
- System Call Tracer(strace)

----------------------------------
First Kernel-generation using KGen
----------------------------------

KGen distribution comes with several examples. Following shows how to run one of examples.

Current version runs only on Linux.

::

    >>> cd $KGEN/examples/simple    # Move to an example
    >>> vi src/Makefile             # Modify FC if required
    >>> make                        # Generate a kernel
    >>> cd kernel                   # Move to a kernel directory
    >>> make                        # Run a kernel

First make command acutally runs a KGen command with several options and an argument. Please see an :doc:`example <examples/simple>` section for details.

