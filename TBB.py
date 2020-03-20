import tkinter as tk
from tkinter import *

#Funtions
def about():
    window = tk.Toplevel(root)
    window.title('About')
    window.iconbitmap("icon.ico")
    S = Scrollbar(window)
    T = Text(window, height=10, width=51, font=("Cambria", 10))
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """The Burning Bush (TBB) is a search engine for religious texts.\nCurrently, the religious texts included are:\n
    \nThis application was made as a project in CSCE 470: Information Storage and Retrieval. It was created by Landon Creel, Hanna\nMitschke, and Sam Stone."""
    T.insert(END, quote)

def search(event=None):
    content = entry.get()
    result = acronym_dictionary.get(content,"Not Found")
    print(result)
    resultBox.delete(0,END)
    resultBox.insert(0,result)

acronym_dictionary={"AKA":"Also known as", "OT":"Overtime"}

#GUI
root = tk.Tk() 
root.title('The Burning Bush')
root.iconbitmap("favicon_v3.ico")
root.geometry('520x440')
root.maxsize(520,440)
root.minsize(520,440)

menu = Menu(root) 
root.config(menu=menu) 
helpmenu = Menu(menu) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About', command=about) 

Label(root, text="Search box:").grid(row=0, sticky=W)
entry = Entry(root)
entry.grid(row=0, column=1)
entry.bind('<Return>', search)
b1 = tk.Button(root, text = "Search", width=12, command=search)
b1.grid(row=0, column=4)
Label(root, text = "Result:").grid(row=1,column=0)
# resultBox = Entry(root)
# resultBox.grid(row=1,column=1)
resultBox = tk.Listbox(root, height=0, width=35)
resultBox.grid(row=1, rowspan=4, columnspan=2)
sb1 = tk.Scrollbar(root)
sb1.grid(row=1, column=3)
resultBox.configure(yscrollcommand=sb1.set)
sb1.configure(command=resultBox.yview)

root.mainloop()