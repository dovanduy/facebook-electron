@echo >>>>>>>>>>>>>>>>>>>>> start <<<<<<<<<<<<<<<<<<<<<<<

set "rar=C:\Program Files\WinRAR\WinRAR.exe"
if  exist *.zip (
    "%rar%" x -ad -y *.zip  D:\python\facebook\ 
) 

wmic environment where "name='PATH' and username='<system>'" set VariableValue="%PATH%;D:\python\facebook\37"

@echo >>>>>>>>>>>>>>>>>>>>> end <<<<<<<<<<<<<<<<<<<<<<<
pause
exit
