@echo off
cd /d %~dp0
set mypath=%cd%
:: echo System Path is: %PATH%
:: echo User Path is: %UserPath%
:: setx PATH gets rid of all other PATH variables for the user
:: /M for the user path
:: setx PATH "%PATH%;%mypath%"
:: set oldpath=reg query HKEY_CURRENT_USER\Environment /v "Path"
:: echo %oldpath%
:: reg add HKEY_CURRENT_USER\Environment /v "BU_Register" /d %mypath%
setx PATH "%PATH%;%mypath%"

del SetupRegister.cmd
