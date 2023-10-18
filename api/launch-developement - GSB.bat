@echo off

call scripts/activate
call conf/developement-GSB.conf.bat
flask run -h 127.0.0.1 -p 80
REM flask run -h 192.168.83.12

pause