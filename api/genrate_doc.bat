@echo off
pdoc --html gsb.py --force
pdoc --pdf gsb.py > readme.md
pause