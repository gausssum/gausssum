from distutils.core import setup
import shutil
import py2exe

version = open("version.txt").next().rstrip()

setup(name="GaussSum",
      version=version,
      author="Noel O'Boyle",
      author_email="baoilleach@users.sf.net",
      url="http://gausssum.sf.net",
      windows = [{'script':'src/GaussSum.py',
                  'icon_resources':[(1, "logo/GaussSum.ico")]}],
      options = {'py2exe': {'dist_dir':'dist/GaussSum-%s' % version,
                            'dll_excludes':['MSVCP80.dll', 'MSVCR80.dll',
                 'OBDLL.dll', 'OBConv.dll', 'oberror.dll', 'OBFPRT.dll'],
                 'excludes': ['_openbabel', 'Bio.KDTree._CKDTree',
                              'Bio.Nexus.cnexus']}},
      data_files = [('.',['src/gausssum/mesh.gif', 'src/gausssum/mesh2.gif',])],
      package_dir = {'gausssum':'src/gausssum'},
      packages=['gausssum','gausssum.cclib','gausssum.cclib.parser']
      )
