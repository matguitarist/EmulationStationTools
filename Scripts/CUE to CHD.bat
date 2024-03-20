for /r %%i in (*.cue, *.gdi *.cdi,*.iso) do chdman createcd -i "%%i" -o "%%~ni.chd"
pause