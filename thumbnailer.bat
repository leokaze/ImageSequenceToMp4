@REM set the path to the python script
set converterPath="P:\Projectos\Proyectos_2024\05-09-LEONARDO - MP4 Rendericer\scripts\thumbnailer.py"

@echo off
set "filepath=%~f1"
echo %filepath%

@REM execute a python script
python %converterPath% %filepath%

pause