import os
import sys
import glob
from cx_Freeze import setup, Executable

version = next(open("../version.txt")).rstrip()

docfiles = glob.glob(os.path.join("..", "docs", "*.html"))
docfiles_dest = [x.replace("..\\docs", "Docs") for x in docfiles]
assert len(docfiles) > 0

setup(name="GaussSum",
      version=version,
      author="Noel O'Boyle",
      author_email="baoilleach@users.sf.net",
      url="http://gausssum.sf.net",
      executables = [Executable('GaussSum.py', base="Win32GUI")],
      options = {"build_exe" : {
          "icon" : "../logo/GaussSum.ico",
          "includes": ["gausssum"],
          "include_files" : [('gausssum/mesh.gif', 'mesh.gif'), ('gausssum/mesh2.gif', 'mesh2.gif')] + list(zip(docfiles, docfiles_dest)),
          "packages":["six"]}}, # Workaround to avoid error message
      )
