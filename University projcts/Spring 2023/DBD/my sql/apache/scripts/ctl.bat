@echo off

if not ""%1"" == ""START"" goto stop

cmd.exe /C start /B /MIN "" "D:\Univercity\DBD\my sql\apache\bin\httpd.exe"

if errorlevel 255 goto finish
if errorlevel 1 goto error
goto finish

:stop
cmd.exe /C start "" /MIN call "D:\Univercity\DBD\my sql\killprocess.bat" "httpd.exe"

if not exist "D:\Univercity\DBD\my sql\apache\logs\httpd.pid" GOTO finish
del "D:\Univercity\DBD\my sql\apache\logs\httpd.pid"
goto finish

:error
echo Error starting Apache

:finish
exit
