from cclib.parser import *
from cclib.utils import *

r = G03("PhCCCC_gopt.out")
r.parse()
r.calcscfprogress()
r.tidyscfprogress().write("scfprogress.txt")
r.calcgeoprogress()
r.tidygeoprogress().write("geoprogress.txt")

t = G03("PhCCCC_pop.out")
t.parse()
t.groups = Groups(t.orbitals,
                  groups={'C6H4':[1,2,3,4,5,6,7,8,19,20],
                          'C=C':[9,10,11,12,13,14,15,16,17,18]},
                  type="atoms")
t.calcpdos()
t.tidypdos().write("orbital_data.txt")
t.calcdosspectrum()
t.tidydosspectrum().write("dosspectrum.txt")
t.calcpdosspectrum()
t.tidypdosspectrum().write("pdosspectrum.txt")

u = G03("PhCCCC_TD.out")
u.pref['uvvis.start'] = 200
u.pref['uvvis.end'] = 500
u.parse()
u.calcuvspectrum()
u.tidyuvspectrum().write("uvspectrum.txt")

v = G03("PhCCCC_IR.out")
v.parse()
v.pref['ir.start'] = 100
v.pref['ir.end'] = 1100
v.calcirspectrum()
v.tidyirspectrum().write("irspectrum.txt")
