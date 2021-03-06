import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
from pathlib import WindowsPath
import sys
from inventory import Inventory

class GUI(tk.Tk):
    def __init__(self, size:tuple, icon_filename:str, banner_filename:str):
        super().__init__()
        self.title('Cellar 97 Inventory Management')
        self.minsize(size[0], size[1])
        self.maxsize(size[0], size[1])
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exit_window)
        self.menubar()
        self.icon(icon_filename)
        self.add_banner(banner_filename)
        self.left_frame = Textbox(self)
        self.bind("<Button-3>", self.right_click_menu )
        self.buttons = Buttons(self)
        self.checkbuttons = Checkbuttons(self)
        self.inventory = Inventory()

    def icon(self, icon_filename):
        icon_path = self.getbasepath(icon_filename)
        self.iconbitmap(default=icon_path)

    def menubar(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Choose Categories", command=lambda:self.checkbuttons.select_categories(self))
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar, bg='#c2c6cc')
    
    def right_click_menu(self, e):
        right_click = tk.Menu(self, tearoff=False)
        right_click.add_command(label='Cut', command=lambda:self.left_frame.cut(self))
        right_click.add_command(label='Copy', command=lambda:self.left_frame.copy(self))
        right_click.add_command(label='Paste', command=lambda:self.left_frame.paste(self))
        right_click.tk_popup(e.x_root, e.y_root)
    
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


class Checkbuttons(tk.Tk):
    def __init__(self, parent):
        self.categories_selected = False
    
    def select_categories(self, parent):
        new_window = tk.Toplevel(parent)
        new_window.details_expanded = False
        new_window.title("Categories")
        new_window.geometry("300x500+{}+{}".format(parent.winfo_x(), parent.winfo_y()))
        new_window.resizable(False, False)
        new_window.rowconfigure(0, weight=0)
        new_window.rowconfigure(1, weight=1)
        new_window.columnconfigure(0, weight=1)
        new_window.columnconfigure(1, weight=1)
        for category in parent.inventory.categories:
            parent.inventory.categories[category] = tk.IntVar()
            tk.Checkbutton(new_window, text=category, variable=parent.inventory.categories[category], onvalue=1, offvalue=0, height=2).pack()
        ttk.Button(new_window, text="OK", command=new_window.destroy).pack()
        self.categories_selected = True


class Buttons(tk.Tk):
    def __init__(self, parent):
        self.import_db_button = tk.Button(parent, text='Import Current DB', command=lambda:self.start_import_database_file(parent) )
        self.import_db_button.place(relx=0.68, rely=0.28)
        self.import_db_button = tk.Button(parent, text='Generate Inventory Report', command=lambda:self.start_inventory_report(parent) )
        self.import_db_button.place(relx=0.68, rely=0.36)
        self.import_db_button = tk.Button(parent, text='Generate Unscanned Items Report', command=lambda:self.start_unscanned_report(parent) )
        self.import_db_button.place(relx=0.68, rely=0.44)
        self.import_db_button = tk.Button(parent, text='Generate Full New Database', command=lambda:self.start_generating_new_db(parent))
        self.import_db_button.place(relx=0.68, rely=0.52)
        self.import_db_button = tk.Button(parent, text='Generate Scanned Item import file', command=lambda:self.start_generating_scanned_item_import(parent))
        self.import_db_button.place(relx=0.68, rely=0.60)
        self.import_db_button = tk.Button(parent, text='List Items not in the Database', command=lambda:self.start_generating_items_not_in_database(parent))
        self.import_db_button.place(relx=0.68, rely=0.68)

    def start_worker_thread(self):
        pass

    def start_import_database_file(self, parent):
        parent.inventory.db_filepath = tkinter.filedialog.askopenfilename \
            (initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        if parent.inventory.db_filepath:
            parent.inventory.import_database_file(parent.inventory.db_filepath)

    def start_inventory_report(self, parent):
        if parent.inventory.import_and_parse_success:
            self.data_from_scanners = parent.left_frame.left_frame_text.get('1.0', tk.END)
            if len(self.data_from_scanners) > 1:
                parent.inventory.generate_inventory_report(self.data_from_scanners)
            else:
                Popup('Please Insert Scanned data')        
        else:
            Popup('Please import a database file')

    def start_unscanned_report(self, parent):
        if parent.inventory.import_and_parse_success:
            self.data_from_scanners = parent.left_frame.left_frame_text.get('1.0', tk.END)
            if len(self.data_from_scanners) > 1:
                parent.inventory.generate_unscanned_report(self.data_from_scanners)
            else:
                Popup('Please Insert Scanned data')
        else:
            Popup('Please import a database file')

    def start_generating_new_db(self, parent):
        if parent.inventory.import_and_parse_success:
            self.data_from_scanners = parent.left_frame.left_frame_text.get('1.0', tk.END)
            if len(self.data_from_scanners) > 1:
                if parent.checkbuttons.categories_selected:
                    for key in parent.inventory.categories:
                        parent.inventory.categories[key] = parent.inventory.categories[key].get()
                    parent.inventory.generate_db_file(self.data_from_scanners)
                else:
                    Popup('Please select categories to change')
            else:
                Popup('Please Insert Scanned data')
        else:
            Popup('Please import a database file')
        

    def start_generating_scanned_item_import(self, parent):
        if parent.inventory.import_and_parse_success:
            self.data_from_scanners = parent.left_frame.left_frame_text.get('1.0', tk.END)
            if len(self.data_from_scanners) > 1:
                    parent.inventory.generate_item_import_file(self.data_from_scanners)
            else:
                Popup('Please Insert Scanned data')
        else:
            Popup('Please import a database file')

    def start_generating_items_not_in_database(self, parent):
        if parent.inventory.import_and_parse_success:
            self.data_from_scanners = parent.left_frame.left_frame_text.get('1.0', tk.END)
            if len(self.data_from_scanners) > 1:
                    parent.inventory.generate_reports_of_items_not_in_database(self.data_from_scanners)
            else:
                Popup('Please Insert Scanned data')
        else:
            Popup('Please import a database file')


class Textbox(tk.Tk):
    def __init__(self, parent):
        self.left_frame = tk.Frame(parent, bg='#dae2f0')
        self.left_frame.place(relx=0.005 ,rely=0.25)
        self.left_frame_scrollbar = tk.Scrollbar(self.left_frame)
        self.left_frame_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_frame_text = tk.Text(self.left_frame, yscrollcommand=self.left_frame_scrollbar.set,  width=50, height=22 , bg='#dae2f0')
        self.left_frame_text.pack()
        self.left_frame_scrollbar.config(command=self.left_frame_text.yview)
        self.left_frame_text.focus()

    def cut(self, parent):
        try:
            selection = self.left_frame_text.get('sel.first', 'sel.last')
        except:
            selection = None
        if selection:
            parent.clipboard_clear()
            parent.clipboard_append(selection)
            self.left_frame_text.delete('sel.first', 'sel.last')
        else:
            text = self.left_frame_text.get('1.0', tk.END)
            self.left_frame_text.delete('1.0', tk.END)
            parent.clipboard_clear()
            parent.clipboard_append(text)

    def copy(self, parent):
        try:
            # selection = self.left_frame_text.selection_get()
            selection = self.left_frame_text.get('sel.first', 'sel.last')
        except:
            selection = None
        if selection:
            parent.clipboard_clear()
            parent.clipboard_append(selection)
        else:
            text = self.left_frame_text.get('1.0', tk.END)
            parent.clipboard_clear()
            parent.clipboard_append(text)
    
    def paste(self, parent):
        clipboard_text = parent.clipboard_get()
        try:
            selection = self.left_frame_text.selection_get()
        except:
            selection = None
        if selection:
            self.left_frame_text.insert('sel.first', clipboard_text)
            self.left_frame_text.delete('sel.first', 'sel.last')
        else:
            self.left_frame_text.insert(tk.END, clipboard_text)


class Popup(tk.Tk):
    def __init__(self, dis_message):
        tkinter.messagebox.showwarning(message=dis_message)

if __name__ == "__main__":
    # current_inventory = Inventory('./csv files/br-union.csv')
    GUI((795, 490), 'cellar97.ico', 'banner.png').mainloop()