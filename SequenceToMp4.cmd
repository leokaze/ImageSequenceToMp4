@REM set the path to the python executable
set converterPath="P:\Projectos\Proyectos_2024\05-09-LEONARDO - MP4 Rendericer\scripts\converter.py"

@REM get the name of the file without extension
@echo off
set "filename=%~n1"
echo %filename%

@echo off
set "filepath=%~f1"
echo %filepath%

@REM execute a python script
python %converterPath% %filepath%

pause