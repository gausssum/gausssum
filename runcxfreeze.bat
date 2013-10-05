@echo off
echo Before you run this, you need to rename C:\Cygwin\bin
echo to C:\Cygwin\oldbin with the 'move' command
pause
cd src
rem "python setup.py build" will just make the build folder if desired
python setup.py bdist_msi
