rem echo off
set ver=2.3
set dist=dist\GaussSum-%ver%
mkdir %dist%

copy src\*.py %dist%
mkdir %dist%\gausssum
copy src\gausssum\*.py %dist%\gausssum
copy src\gausssum\*.gif %dist%\gausssum
mkdir %dist%\gausssum\cclib
mkdir %dist%\gausssum\cclib\parser
copy src\gausssum\cclib\*.py %dist%\gausssum\cclib
copy src\gausssum\cclib\parser\*.py %dist%\gausssum\cclib\parser

copy logo\*.ico %dist%
copy logo\*.gif %dist%

mkdir %dist%\Docs
copy docs\*.html %dist%\Docs
copy docs\*.gif %dist%\Docs
copy docs\*.css %dist%\Docs

cd dist
"C:\Program Files\7-Zip\7z.exe" a -tzip -r -mx=9 GaussSum-%ver%.zip GaussSum-%ver%
cd ..
rmdir /s /q %dist%
