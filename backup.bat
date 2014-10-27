@echo off
if "%1" == "list" (
   python backup.py --list
   goto :eof
)
if "%1" == "add" (
   python backup.py --add %2  --source %3
   goto :eof
)
if "%1" == "remove" (
   python backup.py --remove %2
   goto :eof
)
if "%1" == "dest" (
   python backup.py --destination %2
   goto :eof
)
if "%1" == "delete" (
   python backup.py --delete %2
   goto :eof
)
python backup.py --copy %1

