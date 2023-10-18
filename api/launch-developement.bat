@echo off

call scripts/activate.bat
call conf/developement.conf.bat
flask run -h 127.0.0.1 -p 80
REM flask run -h 192.168.83.10

pause