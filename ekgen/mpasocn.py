import os, subprocess
from microapp import App, appdict
from ekgen.utils import xmlquery

class MPASOcnKernel(App):
    _name_ = "mpasocn"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="dir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="file", help="KGen callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")

        self.register_forward("data", help="json object")

    def perform(self, args):

        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        csname, csext = os.path.splitext(csfile)
        outdir = os.path.abspath(os.path.realpath(args.outdir["_"])) if args.outdir else os.getcwd()

        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        batch = xmlquery(casedir, "BATCH_SYSTEM", "--value")
        if batch == "lsf":
            runcmd += " --batch-args='-K'"
        else:
            raise Exception("Unknown batch system")

 
        compjson = os.path.join(outdir, "compile.json")
        analysisjson = os.path.join(outdir, "analysis.json")
        outfile = os.path.join(outdir, "model.json")
        srcbackup = os.path.join(outdir, "backup", "src")

        # get mpi and git info here(branch, commit, ...)
        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))

        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        # get mpi: mpilib from xmlread , env ldlibrary path with the mpilib
        mpidir = os.environ["MPI_ROOT"]
        excludefile = "/ccs/home/grnydawn/bin/exclude_e3sm_mpas.ini"

        cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --verbose --backup '%s'" % (
                buildcmd, compjson, compjson, srcbackup)
        ret, fwds = self.manager.run_command(cmd)

        # save compjson with case directory map
        # handle mpas converted file for callsitefile2
        # TODO: replace kgen contaminated file with original files
        # TODO: recover removed e3sm converted files in cmake-bld, ... folders

        #cmd = " -- resolve --compile-info '@data' '%s'" % callsitefile
        rescmd = (" -- resolve --mpi header='%s/include/mpif.h' --openmp enable"
                 " --compile-info '%s' --keep '%s' --exclude-ini '%s' '%s'" % (
                mpidir, compjson, analysisjson, excludefile, callsitefile2))
        #ret, fwds = prj.run_command(cmd)
        #assert ret == 0

        # TODO wait??
        cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --cleancmd '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    outdir, cleancmd, buildcmd, runcmd, outfile)
        #ret, fwds = prj.run_command(cmd)
        # add model config to analysis

        cmd = cmd + " -- kernelgen '@analysis' --model '@model' --repr-etime 'ndata=40,nbins=10'  --outdir '%s'" % outdir
        ret, fwds = self.manager.run_command(cmd)

        import pdb; pdb.set_trace()