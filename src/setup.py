import os
import sys
import glob
from cx_Freeze import setup, Executable

version = next(open("../version.txt")).rstrip()

docfiles = glob.glob(os.path.join("..", "docs", "*.html"))
docfiles_dest = [x.replace("..\\docs", "Docs") for x in docfiles]
assert len(docfiles) > 0

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

setup(name="GaussSum",
      version=version,
      author="Noel O'Boyle",
      author_email="baoilleach@users.sf.net",
      url="http://gausssum.sf.net",
      executables = [Executable('GaussSum.py', base="Win32GUI", icon="../logo/GaussSum.ico", shortcutName="GaussSum", shortcutDir = "ProgramMenuFolder")],
      options = {"build_exe" : {
          "includes": ["gausssum",
                       "numpy.core._methods", "numpy.lib.format"], # Missing at runtime
          "include_files" : [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            ('gausssum/mesh.gif', 'mesh.gif'),
            ('gausssum/mesh2.gif', 'mesh2.gif')] + list(zip(docfiles, docfiles_dest)),
          "packages":["six"], # Workaround to avoid error message
          }},
      )
