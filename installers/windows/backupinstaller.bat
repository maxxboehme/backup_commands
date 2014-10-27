@echo off
IF DEFINED BACKUPSCRIPT goto :eof
setx BACKUPSCRIPT "C:\Program Files\BackupScript"
setx PATH "%PATH%;%C:\Program Files\BackupScript;"
REM @echo off&cls
REM setlocal EnableDelayedExpansion
REM set $line=%path%
REM set $line=%$line: =#%
REM set $line=%$line:;= %

REM for %%a in (%$line%) do echo %%a | find /i "oracle" || set $newpath=!$newpath!;%%a
REM set $newpath=!$newpath:#= !
REM echo set path=!$newpath:~1!