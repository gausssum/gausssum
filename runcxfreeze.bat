@echo off
cd src
rem "python setup.py build" will just make the build folder if desired
py setup.py bdist_msi
cd ..
