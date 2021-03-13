#!/usr/bin/bash

CASEDIR=/ccs/home/grnydawn/workbench/E3SM/case
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/cam/src/physics/cam/micro_mg_cam.F90
OUTDIR=/ccs/home/grnydawn/scratch/kernels/atm/ekgen_atm1

ekgen atm $CASEDIR $CALLSITEFILE -o $OUTDIR
