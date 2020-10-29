cd %CD%
copy /Y ..\data_management_system.py .\data_management_system.pyw
pyinstaller -F --windowed  --icon="cellar97.ico" --add-data "banner.png;." --add-data "cellar97.ico;." --onefile --clean "data_management_system.pyw" --name "Cellar 97 Inventory Management.exe"
copy /Y ".\dist\Cellar 97 Inventory Management.exe" "..\DELIVERABLES\Cellar 97 Inventory Management.exe"