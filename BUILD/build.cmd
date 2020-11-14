cd %CD%
copy /Y ..\GUI.py .\GUI.pyw
copy /Y ..\inventory.py .\inventory.pyw
pyinstaller -F --windowed  --icon="cellar97.ico" --add-data "banner.png;." --add-data "cellar97.ico;." --onefile --clean "GUI.pyw" --name "Cellar 97 Inventory Management.exe"
copy /Y ".\dist\Cellar 97 Inventory Management.exe" "..\DELIVERABLES\Cellar 97 Inventory Management.exe"