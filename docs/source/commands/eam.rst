
============================
eam: E3SM Atmospheric Model
============================

Example: kernel extraction from E3SM Atmospheric Model

0. Create a E3SM case
-------------------------

First, create your E3SM case and note the path of this case directory for later use in ekgen run.

1. Mark the kernel region with ekgen directives in source file
----------------------------------------------------------------------------
Choose a file among EAM files.

2. run ekgen
--------------------
Make directory for the kernel generation. Or you can specify the output directory using "-o" ekgen option. Run ekgen-eam with case directory path and ekgen-directed source file path.

3. check extracted kernel source files and data files
---------------------------------------------------------------
Once completed kernel extraction successfully, "kernel" directory will be created in the output directory with source files, data files, and a Makefile. You may try to build/run the kernel as following:


> cd kernel
> make build
> make run
 

The extracted kernel has a built-in timing measurement and correctness check that ensure the kernel generates the same data that the original application generates. Following is a partial capture of screen output when the gm_bolus_velocity kernel runs.
