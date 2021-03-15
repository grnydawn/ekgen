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

-------------------------
E3SM Kernel Extraction
-------------------------

Once ekgen is installed correctly and a E3SM case is created successfully, you can extract a kernel as exaplained below.

The syntax of ekgen command is following:

        >>> ekgen <mpasocn|eam> $CASEDIR $CALLSITEFILE

, where $CASEDIR is a directory path to E3SM case directory and $CALLSITEDIR is a file path to a E3SM source file containing ekgen kernel region directives.
As of this version, there exist two subcommands of mpasocn and eam for MPAS Ocean Model and E3SM Atmospheric Model each. Please see _command for details about the sub-commands.

ekgen kernel region directives a pair of comment-line directives that defines a region of kernel extraction. Following example 

::

        !$kgen begin_callsite vecadd
        DO i=1
                C(i) = A(i) + B(i)
        END DO
        !$kgen  end_callsite

Please see _directives for details about using ekgen directives.
