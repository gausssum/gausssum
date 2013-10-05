@echo off
cd src
rem "python setup.py build" will just make the build folder if desired
python setup.py bdist_msi
cd ..
