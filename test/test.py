import os
import sys
import nose
import math
import shutil
import tkinter
import collections

gausssumdir = os.path.join("..")
sys.path.append(os.path.join(gausssumdir, "src"))
version = open(os.path.join(gausssumdir, "version.txt")).read().rstrip()
ver = ".".join(version.split(".")[:2])
root = tkinter.Tk()

from gausssum.electrontrans import ET
from gausssum.popanalysis import Popanalysis
from gausssum.vibfreq import Vibfreq, get_scaling_factors
from gausssum.cclib.parser import ccopen
from gausssum.cclib.parser.utils import convertor
from gausssum.utils import Groups

def clearoutput(filename):
    gdir = gaussdir(filename)
    if os.path.isdir(gdir):
        shutil.rmtree(gdir)

def parse(filename):
    log = ccopen(filename)
    log.logger.setLevel(50) # (logging.ERROR)
    return log.parse()
    
def runone(filename):
    clearoutput(filename)
    data = parse(filename)

    ET(None, sys.stdout, data, filename, 200, 500, 500, 3000, True,
       None, False)
    sys.exit()

def gaussdir(filename):
    return os.path.join(os.path.dirname(filename), "gausssum%s" % ver)

def helptestTDDFT(filename, result):
    clearoutput(filename)
    data = parse(filename)

    root = tkinter.Tk()

    ET(None, sys.stdout, data, filename, 200, 500, 500, 3000, True,
       None, False)

    contribs = [x for x in open(os.path.join(gaussdir(filename), "UVData.txt"))
                if x.startswith("1")][0]
    maincontribs = contribs.split("\t")[5]
    assert maincontribs == result, "\n   %s\nis not equal to\n   %s" % (maincontribs, result)

def test_ECCD():
    filename = os.path.join("exampleCircularDichroism", "OPT_td.out")
    clearoutput(filename)
    data = parse(filename)

    Sigma = 2.402185 # Because it corresponds to a FWHM of 2.0
    ET(None, sys.stdout, data, filename, 100, 300, 10000, Sigma, False,
       None, False)

    spectrum = [list(map(float, x.split()[:3])) for x in open(os.path.join(gaussdir(filename), "CDSpectrum.txt")) if not x[0]=="E"]

    # Assert Peak Max
    maxval = max([x[2] for x in spectrum])
    assert abs(maxval - 0.143 ) < 0.001

    # Assert Sigma...(full width at 1/e height)
    one_over_e_max = maxval / math.e
    for x,y,z in spectrum:
        if abs(z - one_over_e_max) < 0.00002:
            one_over_e_x = x
        if z == maxval:
            max_x = x
    fullwidth = (one_over_e_x - max_x) * 2.
    width_in_eV = fullwidth / convertor(1., "eV", "cm-1")
    
    assert abs(width_in_eV - Sigma) < 0.01


def test_R_TDDFT():
    filename = os.path.join("exampleTDDFT", "benzene_tddft_more.out")
    result = "H-1->L+1 (52%), HOMO->LUMO (52%)"
    helptestTDDFT(filename, result)

def test_U_TDDFT():
    filename = os.path.join("exampleTDDFT", "benzene_trip_tddft.out")
    result = "HOMO(B)->LUMO(B) (115%)"
    helptestTDDFT(filename, result)

def test_R_TDHF():
    filename = os.path.join("exampleTDHF", "benzene_tddft_more.out")
    result = "H-1->LUMO (62%), HOMO->L+1 (62%)"
    helptestTDDFT(filename, result)

def test_U_TDHF():
    filename = os.path.join("exampleTDHF", "benzene_trip_tddft.out")
    result = "H-1(B)->L+2(B) (10%), HOMO(B)->LUMO(B) (141%)"
    helptestTDDFT(filename, result)

def test_IR():
    filename = os.path.join("exampleIR", "benzene_ir.out")
    clearoutput(filename)
    data = parse(filename)

    Vibfreq(None, sys.stdout, data, filename, 1000, 2000, 100, 5,
            "Gen", 1.0, 785, 293.15,
            None)

    assert os.path.isfile(os.path.join("exampleIR", "gausssum%s" % ver, "IRSpectrum.txt"))
    assert os.path.isfile(os.path.join("exampleIR", "gausssum%s" % ver, "RamanSpectrum.txt"))

    # Add scaling factors
    for name in ["IR", "Raman"]:
        with open("test%s.txt" % name, "w") as f:
            for i, line in enumerate(open(os.path.join("exampleIR", "gausssum%s" % ver, "%sSpectrum.txt" % name), "r")):
                broken = line.split("\t")
                if i > 2 and len(line) > 4:
                    broken[-2] = "%f" % (i*0.2,)
                f.write("\t".join(broken))
    
    # Check that they can be read
    for name in ["IR", "Raman"]:
        scale = collections.defaultdict(int) # Duck-typing to pretend it's a list        
        filename = os.path.join("test%s.txt" % name)
        get_scaling_factors(filename, scale)
        assert abs(scale[0] - 1.0) < 0.0001
        assert abs(scale[1] - 0.6) < 0.0001

def test_MO_contribs():

    data = [
        (True, "benzene_trip_pop.out", "benzene_trip_tddft_2.out",
         ["66", "L+44", "60.33", "?", "66", "L+45", "60.57", "?"],
         ["66", "34", "66", "34"],
         "HOMO(B)->LUMO(B) (100%)",
         ["59-->75 (16)", "41-->25 (-16)"]
         ),

        (False, "benzene_pop.out", "benzene_tddft_2.out",
         ["66", "L+44", "67.32", "B1u"],
         ["67", "33"],
         "H-1->L+1 (50%), HOMO->LUMO (50%)",
         ["67-->67 (0)", "33-->33 (0)"]
         )
        ]

    for unres, popfile, tdfile, mos, mocontribs, excitations, change in data:
        filename = os.path.join("exampleTDDFT", popfile)
        clearoutput(filename)
        data = parse(filename)

        # Without groups.txt
        Popanalysis(None, sys.stdout, data, filename, -20, 0, False, 0.3, False, None)
        assert os.path.isfile(os.path.join("exampleTDDFT", "gausssum%s" % ver, "orbital_data.txt"))
        with open(os.path.join("exampleTDDFT", "gausssum%s" % ver, "orbital_data.txt")) as f:
            while True:
                line = next(f)
                if line.find("L+") >= 0: break
            assert line.rstrip() == "\t".join(mos)

        # With groups.txt
        with open(os.path.join("exampleTDDFT", "gausssum%s" % ver, "Groups.txt"), "w") as f:
            f.write("\n".join(["atoms", "First", "1-3", "Second", "4-12"]))
        Popanalysis(None, sys.stdout, data, filename, -20, 0, False, 0.3, False, None)
        assert os.path.isfile(os.path.join("exampleTDDFT", "gausssum%s" % ver, "orbital_data.txt"))
        with open(os.path.join("exampleTDDFT", "gausssum%s" % ver, "orbital_data.txt")) as f:
            while True:
                line = next(f)
                if line.find("L+") >= 0: break
            line = line.rstrip().split()
            assert line[0:4] == mos[:4]
            print(line[4:6])
            print(mocontribs[:2])
            assert line[4:6] == mocontribs[:2]
            if unres:
                assert line[8:12] == mos[4:]
                assert line[12:14] == mocontribs[2:]

        # Now parse the corresponding TDDFT file
        filename = os.path.join("exampleTDDFT", tdfile)
        data = parse(filename)
        ET(None, sys.stdout, data, filename, 200, 500, 500, 3000, True,
           None, False)
        assert os.path.isfile(os.path.join("exampleTDDFT", "gausssum%s" % ver, "UVData.txt"))
        with open(os.path.join("exampleTDDFT", "gausssum%s" % ver, "UVData.txt")) as f:
            while True:
                line = next(f)
                if line.find("Wavelength") >= 0:
                    break
            line = next(f).rstrip().split("\t")
            assert line[5] == excitations
            assert line[7:9] == change

def test_groups():
        filename = os.path.join("exampleTDDFT", "benzene_pop.out")
        data = parse(filename)
        ans = {"First":list(range(0, 20)), "Second": list(range(20, 66))}
        
        examples = [["atoms", "First", "1-3", "Second", "4-12"],
                    ["atoms", "  First", "1-3", "Second", "   4-12"],
                    ["", "atoms", "  First", "1-3", "Second", "   4-12"],
                    ["atoms", "  First", "1-3", "Second", "   4-12", "" , ""]]
        for example in examples:
            filename = os.path.join("exampleTDDFT", "gausssum%s" % ver, "Groups.txt")
            with open(filename, "w") as f:
                f.write("\n".join(example))
            groups = Groups(filename, data.atomnos, data.aonames, data.atombasis)

            assert groups.groups == ans



if __name__ == "__main__":

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        runone(filename)

    nose.main()

