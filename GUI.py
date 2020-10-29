import tkinter as tk
import tkinter.ttk as ttk
from pathlib import WindowsPath
import sys
import inventory
from openpyxl.descriptors.base import Default

class GUI(tk.Tk):
    def __init__(self, inventory:inventory.Inventory, size:tuple, icon_filename:str, banner_filename:str):
        super().__init__()
        self.title('Cellar 97 Inventory Management')
        self.minsize(size[0], size[1])
        self.maxsize(size[0], size[1])
        self.resizable(0, 0)

        self.protocol("WM_DELETE_WINDOW", self.exit_window)
        
        self.icon(icon_filename)
        self.add_banner(banner_filename)
        

        self.menubar()

    def icon(self, icon_filename):
        icon_path = self.getbasepath(icon_filename)
        self.iconbitmap(default=icon_path)

    def menubar(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Log File Folder")
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar, bg='#c2c6cc')
    
    def add_banner(self, banner_filename):
        banner_path = self.getbasepath(banner_filename)
        banner = tk.PhotoImage(file=banner_path)
        background_label = tk.Label(self, image=banner, borderwidth=0, highlightthickness=0)
        background_label.photo = banner
        background_label.place( relx=0.00, rely=0.00)

    def yes_exit(self):
        print("do other stuff here then self.destroy")
        self.destroy()

    def getbasepath(self, file):
        try:
            return WindowsPath(sys._MEIPASS, file)
        except:
            return file

    def exit_window(self):
        top = tk.Toplevel(self)
        top.details_expanded = False
        top.title("Quit")
        top.geometry("300x100+{}+{}".format(self.winfo_x(), self.winfo_y()))
        top.resizable(False, False)
        top.rowconfigure(0, weight=0)
        top.rowconfigure(1, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        tk.Label(top, image="::tk::icons::question").grid(row=0, column=0, pady=(7, 0), padx=(7, 7), sticky="e")
        tk.Label(top, text="Are you sure you want to quit?").grid(row=0, column=1, columnspan=2, pady=(7, 7), sticky="w")
        ttk.Button(top, text="OK", command=self.yes_exit).grid(row=1, column=1, sticky="e")
        ttk.Button(top, text="Cancel", command=top.destroy).grid(row=1, column=2, padx=(7, 7), sticky="e")

if __name__ == "__main__":
    current_inventory = inventory.Inventory('./csv files/br-union.csv')
    GUI(current_inventory, (795, 490), 'cellar97.ico', 'banner.png').mainloop()