.. ekgen documentation master file, created by
   sphinx-quickstart on Wed Mar 10 14:45:17 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================================
ekgen: E3SM Kernel Extraction and Analysis
=================================


Welcome to the E3SM Kernel Extraction and Analysis (ekgen).

ekgen is a kernel extraction and analysis tool customized for the Energy Exascale Earth System Model (E3SM). The ekgen is a Python module and command-line tool that can be downloaded using the Python package manager (pip). With ekgen, a user can extract a part of E3SM code and make the extracted code(kernel) compilable independently from the E3SM. The ekgen also generate input data to drive the kernel execution and out-type data to verify the correctness of the execution. With combined the extracted kernel code and generated data, user can perform various software engineering tasks such as performance optimization, GPU porting, simulation validation, debugging, unit testing, and more without depending on the E3SM as well as the system.

As of this version, the ekgen supports MPAS Ocean and EAM component models.

The ekgen is an E3SM-specialized version of a more generic Kerne Extraction and Analsys Framework explained in next section.


Kernel extraction and analysis framework
-------------------------------------------------

The automated kernel extraction is based on static analysis of an application source code. When a user provides the ekgen with a range of code for extraction, it parses the code to Abstract Syntax Tree (AST) and see if all code statements required to compile the part of code exists within the AST. If yes, it stops the analysis and convert the collected ASTs to source code. If not, it reads another source files based on information found in Fortran USE statement, and tries to find all statements that make the the range of code compilable, and continue.

While the above basic functionalities for kernel extraction are the same to the ekgen kernle extraction, in general, there are subtle differences between application in terms of building system, Fortran standard used, complexity of the code, and so on, which make it hard for one version of a kernel traction tool to support. For these reasons, a framework for kernel extraction is developed as a core function. Each version that supports a specific application is a kind of wrapper with custom configuration of the framework.


In the following section, benefits of using a kernel are explained.


Kernel-based software engineering approach
------------------------------------------------

what is a kernel
benefits of using kernel instead of full application
Why is important to do kernel based software engineering approach

What are real success cases

how to generate a kernel
Automated kernel extraction


.. only:: html

    :Release: |version|
    :Date: |today|

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro 
   commands/index
   examples/index
   developer/index





ekgen-mpasocn Fortran kernel extractor
Created by Youngsung Kim
Last updated Feb 19, 20214 min read6 people viewed6 people viewedAttachmentsAttachments
ekgen-mpasocn is an app running on ekgen kernel extraction platform. It is customized for extracting Fortran kernel from E3SM MPAS Ocean model. ekgen is a Fortran kernel extraction platform customized for E3SM simulation software.

  Getting Started
Prerequisite
ekgen is written in Python.

Python 2.7+ or Python 3.5+

E3SM

Installation
The easiest way to install ekgen is to use pip python package manager. 

>>> pip install ekgen

You can install ekgen from github code repository if you want to try the latest version.

>>> git clone https://github.com/grnydawn/ekgen.git - Connect to preview 

>>> cd ekgen

>>> python setup.py install

Once installed, you can test the installation by running following command.

>>> ekgen --version

ekgen 0.1.0

  Example: kernel extraction from E3SM MPAS Ocean
0. Create a E3SM case
First, create your E3SM case and note the path of this case directory for later use in ekgen run.

1. Mark the kernel region with ekgen directives in source file
Choose a file among MPAS Ocean source files. In this example, we marked ekgen directives in “components/mpas-source/src/core_ocean/shared/mpas_ocn_gm.F”


#### mpas_ocn_diagnostics.F#####

module ocn_gm
...
subroutine ocn_gm_compute_Bolus_velocity(diagnosticsPool, meshPool, scratchPool)
...   
      allocate(rightHandSide(nVertLevels))
      allocate(tridiagA(nVertLevels))
      allocate(tridiagB(nVertLevels))
      allocate(tridiagC(nVertLevels))

!$kgen begin_callsite gm_bolus_velocity

      nCells = nCellsArray( size(nCellsArray) )
      nEdges = nEdgesArray( size(nEdgesArray) )
...
      !$omp do schedule(runtime)
      do iCell = 1, nCells
         gmStreamFuncTopOfCell(:, iCell) = gmStreamFuncTopOfCell(:,iCell) / areaCell(iCell)
      end do
      !$omp end do

!$kgen end_callsite gm_bolus_velocity
...
end subroutine ocn_gm_compute_Bolus_velocity
...
end module ocn_gm
2. run ekgen
Make directory for the kernel generation. Or you can specify the output directory using “-o” ekgen option. Run ekgen-mpasocn with case directory path and ekgen-directed source file path.


> mkdir ocn_gm_kernel
> cd ocn_gm_kernel
> ekgen mpasocn ${HOME}/scratch/mycase ${HOME}/scratch/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_gm.F
ekgen-mpasocn run initiates one E3SM build and two E3SM runs with additional analysis overheads. Therefore, it is advised to wait up to 2 ~ 3 times of your regular E3SM build/run time including time to wait on job queue.

3. check extracted kernel source files and data files
Once completed kernel extraction successfully, “kernel” directory will be created in output directory with source files, data files, and a Makefile. You may try to build/run the kernel as following:

 


> cd kernel
> make build
> make run
 

The extracted kernel has a built-in timing measurement and correctness check that ensure the kernel generates the same data that the original application generates. Following is a partial capture of screen output when the gm_bolus_velocity kernel runs.

…

#***************** Verification against 'gm_bolus_velocity.16.0.2' *****************

Number of output variables:            43
Number of identical variables:            43
Number of non-identical variables within tolerance:             0
Number of non-identical variables out of tolerance:             0
Tolerance:    1.0000000000000000E-014

Verification PASSED with gm_bolus_velocity.16.0.2

gm_bolus_velocity : Time per call (usec):     47257.00000000000

#****************************************************
kernel execution summary: gm_bolus_velocity
#****************************************************
Total number of verification cases  :    42
Number of verification-passed cases :    42

kernel gm_bolus_velocity: PASSED verification

number of processes  1

Average call time (usec):  0.411E+05
Minimum call time (usec):  0.267E+05
Maximum call time (usec):  0.499E+05

#****************************************************

4. Note on this version of ekgen
ekgen and ekgen-mpaocn are under development. I am happy to support you if you have any issue on extracting kernels from E3SM MPAS Ocean and other E3SM components. Please contact me to “kimy@ornl.gov” if you have any question. 

  ekgen-mpasocn user’s guide
ekgen-mpasocn is a version of ekgen that is a Fortran kernel generator customized for E3SM simulation software.

1. Marking ekgen directives in source file
The kernel region for extraction can be specified by placing following two ekgen directives right above and below of the kernel code region.

 

!$kgen begin_callsite <kernel_name>
This directive indicates that kernel region begins after this directive. The <kernel_name> is used in the generated kernel.

 

!$kgen end_callsite [kernel_name]
This directive indicates that kernel region ends just before this directive. The <kernel_name] is optional.

 

Example of directive usage

!$kgen begin_callsite vecadd
DO i=1
    C(i) = A(i) + B(i)
END DO
!$kgen  end_callsite
 

Notes on placing the ekgen directives
There are following limitations on placing ekgen directives in source file.

the ekgen directives should be placed within executable construct. For example, the directives can not be placed in specification construct such as “use mpi” and “integer(8) i, j, k”.

the ekgen directives can not placed across block boundaries. For example, following usage is not allowed.

To extract a kernel that contains any communication or file system access inside, additional ekgen directives should be used,  which are not documented yet.

 


DO i=1
    !$kgen begin_callsite vecadd  #### NOT VALID : across DO block boundary
    C(i) = A(i) + B(i)
END DO
!$kgen  end_callsite #### NOT VALID : across DO block boundary
2. Command line usage
usage: ekgen mpasocn [-h] [--version] [-o OUTDIR] casedir callsitefile

 

casedir
directory path to E3SM case directory

 

callsitefile
file path to the source file that contains ekgen callsite directives

 

[-o OUTDIR]
directory path in that kernel output files and data will be created

[-h]
print help message

Contact: Youngsung Kim <kimy@ornl.gov>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
