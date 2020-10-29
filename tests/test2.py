from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import threading
import subprocess
import os
import datetime
import re
from shutil import copy

#Global Vars
pdf_file_directory = ''
files_to_process_with_location = []
files_to_tj_number = {} #matches a file to a TJ number for moving

def help():
    """Help popup window explaining how to use program"""
    # create a pop up with usage instructions
    help_dialog = 'This is a program made to copy monthly Account Summaries to I drive.\n'
    help_dialog += '\nPlease ask IT support to create the UNC path before using:'
    help_dialog += ' //192.168.1.31/Titan/Titan/Projects/\n'
    help_dialog += ' \nTo Use: First select the folder where the PDF reports are saved'
    help_dialog += ' then just click move files and the program will file them to I drive'
    showinfo("Useful Information", help_dialog)

def open_dir():
    """Opens the Directory with the log file"""
    cwd = os.getcwd()
    subprocess.call("explorer " + cwd, shell=True)

def select_directory():
    """Selects the directory where all the files are and appends them to a global list to process later"""
    global pdf_file_directory
    global files_to_process_with_location
    pdf_file_directory = filedialog.askdirectory()
    for pdf in os.listdir(pdf_file_directory):
        if pdf[-3:] == 'pdf':
            files_to_process_with_location.append(pdf_file_directory + '/' + pdf)
            left_frame_listbox.insert(END, pdf)
            left_frame_listbox.yview(END)
            left_frame_listbox.update()

def transfer_to_right_frame(file_path):
    """Transfers information from one frame to the other"""
    file_name = file_path.split('/')[-1]
    idx = left_frame_listbox.get(0, END)
    for i in range(len(idx)):
        if file_name in idx[i]:
            left_frame_listbox.delete(i)
            left_frame_listbox.update()
            right_frame_listbox.insert(END, file_name)
            right_frame_listbox.yview(END)
            right_frame_listbox.update()

def find_file_path_using_UNC(tj_num):
    """Returns a File path from a given TJ number"""
    year = '20' + tj_num[2:4]
    uncpath = '//192.168.1.31/Titan/Titan/Projects/{}/'.format(year)
    for item in os.listdir(uncpath):
        if tj_num in item:
            path = uncpath + item + '/Docs/Billing/'
            break    
    return path

def move_files_thread_start():
    threading.Thread(target=move_files_to_directory).start()

def transfer_to_right_frame_thread_start(file_path):
    threading.Thread(target=transfer_to_right_frame, args=(file_path,)).start()

def move_files_to_directory():
    """ Moves the files from the selected directory to TJ Number + Docs + Billing"""
    global files_to_process_with_location
    # start the logging process on the root file location
    logtime = datetime.datetime.now()
    log = open(logtime.strftime("%Y-%m-%d") + '.log', 'a')
    # log.write(logtime.strftime("%H:%M:%S%p") + " Log Start\n")

    if len(files_to_process_with_location) != 0:
        for pdf_file in files_to_process_with_location:
            tj_number = re.search(r"(TJ|tj)[0-9]{5}(\.[0-9]{2})?([a-zA-Z]{2})?", pdf_file)
            if tj_number:
                files_to_tj_number[pdf_file] = tj_number.group()
            else:
                log.write(logtime.strftime("%H:%M:%S%p ") + 'TJ Number was not found in filename: ' + pdf_file)
                # print('The Tj number was not found in the file')
                continue # skip this file because we cannot find TJ Number
            try:
                path_to_move_file = find_file_path_using_UNC(files_to_tj_number[pdf_file])
            except FileNotFoundError:
                # log an error
                log.write(logtime.strftime("%H:%M:%S%p ") + 'Access to I drive not working\n')
                log.close()
                return
            except:
                log.write(logtime.strftime("%H:%M:%S%p ") + 'cannot parse TJ number\n')
                log.close()

            # print(path_to_move_file)
            logging_data = 'moving file: %s to: %s \n' % (pdf_file, path_to_move_file) 

            try:
                copy(pdf_file, path_to_move_file)
                transfer_to_right_frame(pdf_file)
                log.write(logtime.strftime("%H:%M:%S%p ") + logging_data)
            except:
                log.write(logtime.strftime("%H:%M:%S%p ")+ 'Failed to Move File' + logging_data +'\n')
                log.close()
                return
            
    files_to_process_with_location = []
    log.close()

root = Tk()
root.title('Account Summary Filing Program v0.8')
root.minsize(1366, 610)
root.maxsize(1366, 610)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Help", command=help)
filemenu.add_command(label="Open Log File Folder", command=open_dir)
filemenu.add_separator()
filemenu.add_command(label="Close", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

# Right Frame for data to be processesd
left_frame = Frame(root, bg='white')
left_frame.place(relx=0.005 ,rely=0.40)
left_frame_scrollbar = Scrollbar(left_frame)
left_frame_scrollbar.pack(side=RIGHT, fill=Y)
left_frame_listbox = Listbox(left_frame, yscrollcommand= left_frame_scrollbar.set,  width=108, height=22)
left_frame_listbox.pack(side=LEFT)
left_frame_scrollbar.config(command=left_frame_listbox.yview)

# Left Frame for data already processed
right_frame = Frame(root, bg='white')
right_frame.place(relx=0.505 ,rely=0.40)
right_frame_scrollbar = Scrollbar(right_frame)
right_frame_scrollbar.pack(side=RIGHT, fill=Y)
right_frame_listbox = Listbox(right_frame, yscrollcommand= right_frame_scrollbar.set,  width=108, height=22)
right_frame_listbox.pack(side=LEFT)
right_frame_scrollbar.config(command=right_frame_listbox.yview)

select_directory_button = Button(root, text='Select folder', command=select_directory)
select_directory_button.place(relx=0.60, rely=0.15)
move_files_button = Button(root, text='Move Files', command=move_files_thread_start)
move_files_button.place(relx=0.60, rely=0.22)

root.config(menu=menubar, bg='#02263E')
root.mainloop()