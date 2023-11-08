
@echo off
timeout /t 20 >nul

set "folder_path=E:\SB_Runtimeapi_Automation_Beta\Runtime_Scripts"
set "file_name=uiux.txt"

echo This is some content for the text file. > "%folder_path%\%file_name%"

echo Text file '%file_name%' created in '%folder_path%'