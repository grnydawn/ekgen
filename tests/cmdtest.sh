#!/usr/bin/bash

CASEDIR=/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20210125_094617_kmwz7r
#CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_tracer_advection_std.F
CALLSITEFILE=/ccs/home/grnydawn/repos/github/E3SM/components/mpas-source/src/core_ocean/shared/mpas_ocn_effective_density_in_land_ice.F
OUTDIR=/ccs/home/grnydawn/scratch/kernels/ocn/ekgen_1

ekgen mpasocn $CASEDIR $CALLSITEFILE -o $OUTDIR
