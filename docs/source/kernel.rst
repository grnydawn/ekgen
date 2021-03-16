.. _kernel-index:

*****************
Marking a kernel
*****************

A user can specify the kernel region by placing two ekgen comment-line directives before and after the region.


**!$kgen begin_callsite <kernel_name>**
This directive indicates that the kernel region begins after this directive. The <kernel_name> is used in the generated kernel.


**!$kgen end_callsite [kernel_name]**
This directive indicates that the kernel region ends just before this directive. The <kernel_name] is optional.


Example of directive usage
--------------------------------

.. code-block:: fortran

        !$kgen begin_callsite vecadd
        DO i=1
            C(i) = A(i) + B(i)
        END DO
        !$kgen  end_callsite
 

Notes on placing the ekgen directives
--------------------------------------------

There are following limitations on placing ekgen directives in source file.

        * the ekgen directives should be placed within the executable constructs. For example, the directives can not be placed in specification construct such as use mpi and integer(8) i, j, k.

        * To extract a kernel that contains any communication or file system access inside, additional ekgen directives should be used,  which are not documented yet.

        * the ekgen directives can not be placed across block boundaries. For example, following usage is not allowed.

.. code-block:: fortran

        DO i=1
        !$kgen begin_callsite vecadd  #### NOT VALID : across DO block boundary
                C(i) = A(i) + B(i)
        END DO
        !$kgen  end_callsite #### NOT VALID : across DO block boundary 

