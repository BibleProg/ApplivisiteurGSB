@echo off

call scripts/activate.bat
call conf/production.conf.bat
flask run -h 127.0.0.2 -p 80

pause