@echo off

call scripts/activate.bat
call conf/developement-GSB.conf.bat
REM flask run -h 127.0.0.1 -p 80
flask run -h 192.168.83.12

pause