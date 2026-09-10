@echo off

REM activating the python virtual environment
cd C:\labelstudioenv\Scripts
call activate

REM setting label studio variables
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=C:\\borescope-yolo-training\\data

REM Launch label studio
label-studio
pause