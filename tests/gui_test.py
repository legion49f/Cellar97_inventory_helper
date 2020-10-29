import tkinter as tk

def insert_text(text:str):
    print(text)

root = tk.Tk()
S = tk.Scrollbar(root)
T = tk.Text(root, height=4, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
# T.insert(tk.END, '')
B = tk.Button(text='prees me', command= lambda: insert_text(T.get("1.0", tk.END)) ) 
B.pack()
tk.mainloop()