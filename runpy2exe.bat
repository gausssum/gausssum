@echo off
echo Before you run this, you need to rename C:\Cygwin\bin
echo to C:\Cygwin\oldbin with the 'move' command
pause
set /p myver=<version.txt
echo GaussSum version is %myver%

rmdir /s /q dist\GaussSum-%myver%
python -V 
python setup.py py2exe

cd dist
mkdir GaussSum-%myver%\gnuplot460
xcopy /e ..\src\gnuplot460 GaussSum-%myver%\gnuplot460
mkdir GaussSum-%myver%\Docs
copy ..\docs\*.html GaussSum-%myver%\Docs
copy ..\docs\*.gif GaussSum-%myver%\Docs
copy ..\docs\*.css GaussSum-%myver%\Docs

if exist GaussSumexe-%myver%.zip del GaussSumexe-%myver%.zip
"C:\Program Files\7-Zip\7z" a -tzip -r -mx=9 GaussSumexe-%myver%.zip GaussSum-%myver% -ir!GaussSum-%myver%\*
rmdir /s /q GaussSum-%myver%
cd ..
