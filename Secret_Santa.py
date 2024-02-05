# This program implements a name randomizer and matching algorithm.
#
# Copyright (C) 2024 -  Oliver Mihok
#
# This program is a free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
╔═══╗──────────╔╗─╔═══╗─────╔╗
║╔═╗║─────────╔╝╚╗║╔═╗║────╔╝╚╗
║╚══╦══╦══╦═╦═╩╗╔╝║╚══╦══╦═╬╗╔╬══╗
╚══╗║║═╣╔═╣╔╣║═╣║─╚══╗║╔╗║╔╗╣║║╔╗║
║╚═╝║║═╣╚═╣║║║═╣╚╗║╚═╝║╔╗║║║║╚╣╔╗║
╚═══╩══╩══╩╝╚══╩═╝╚═══╩╝╚╩╝╚╩═╩╝╚╝
"""


import os, sys, shutil, random
import os.path
import tkinter as tk
from tkinter import *
from tkinter import Menu
from tkinter import messagebox
import tempfile


list_of_names = []


def folders(x):
    """
    Creating folders to store files (lists and names)
    """
    if x == 1:
        list_folder = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Lists')
        if not os.path.exists(list_folder):
            os.makedirs(list_folder)

    elif x == 2:
        names_folder = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Names')
        if not os.path.exists(names_folder):
            os.makedirs(names_folder)
    else:
        tk.messagebox.showinfo('WRONG', 'FOLDERS() main ELSE!')
        pass


def check_saves():
    for n in range(1, 4):
        file_path = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Lists', f'list_{n}.txt')
        if os.path.exists(file_path):
            load_menu.entryconfig(n-1, label="Slot - " + str(n) + " #")
            if os.path.getsize(file_path)<int(1):
                os.remove(file_path)           
                load_menu.entryconfig(n-1, label="Slot - " + str(n)) 


def save(slot):
    """
    Save lists
    """
    list_folder = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Lists')
    if not os.path.exists(list_folder):
        os.makedirs(list_folder)
        
    menu_numbers = ['1', '2', '3']
    load_menu_labels = ["Slot - 1", "Slot - 2", "Slot - 3"]
    load_menu_index = menu_numbers.index(slot)
    load_menu_label = load_menu_labels[load_menu_index]
    info_message.set(f'Saving to List {slot}.')
    file_name = os.path.join(list_folder, f'list_{slot}.txt')


    with open(file_name, 'w', encoding='utf-8') as f:
        for entry in list_of_names:
            f.write(entry + '\n')

    check_saves()
    info_message.set(f'List {slot} saved.')


def load(choose_list):
    """
    Load the saved name lists.
    """
    try:
        list_file_path = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Lists', f'list_{choose_list}.txt')
        if choose_list in ['1', '2', '3']:
            with open(list_file_path, 'r') as r:
                new()
                for entry in r:
                    list_of_names.append(entry.rstrip())
                    name_list.insert(END, str(entry))
                info_message.set(f'Slot - {choose_list} is loaded')
        else:
            tk.messagebox.showinfo('WRONG', 'LOAD() main ELSE!')
    except (FileNotFoundError, IOError):
        tk.messagebox.showinfo('Missing', 'Cannot find the file.')


def help_me():
    Message = """
    This app shuffles the names and save them as text files.
    It saves secret santa's names to files.
    The text file contains the name of the person to be gifted
    
    1 - Type the name in the input box, then press enter
    2 - Repeat as many time as you wish to add new names
    3 - Click on "Magic" button for Santa to create your files

    This will get the names paired and save them into files.
    "../Temp/Secret Santa/Names/" folder contain the files.
    
    To delete a name select the it then right click on it.
    If you don't select a name, the top name will be deleted.
    """
    tk.messagebox.showinfo("Help Page", Message)


def get_name(name):
    """
    Validates the name exceptions
    """
    if name == '':
        info_message.set('Please type a name, then press enter.')
        return False
    elif len(name) < 2:
        info_message.set('The name has to be at least 2 letters long.')
        return False
    elif not name.isalpha() and len(name) < 3:
        info_message.set('A number or special key is available after the second letter.')
        return False
    elif name.isnumeric():
        info_message.set('The name cannot be a number.')
        return False
    else:
        if name in list_of_names:
            info_message.set('This name is already taken.')
            return False
        else:
            list_of_names.append(name)
            info_message.set(name + ' is added to the list.')
            return True


def shuffle():
    """
    Checks if the list is not empty
    Creates text files with the name of secret santa.
    Store names in list so it can be managed.
    The program checks if the paired names are not the same.
    """
    if len(list_of_names) == 0:
        info_message.set('There are no names entered to be paired.')
    else:
        temp_list = list_of_names.copy()
        folders(2)
        i = 0
        while i < len(list_of_names):
            pair = temp_list.pop(random.randrange(len(temp_list)))
            if str(list_of_names[i]) == str(pair):
                temp_list.insert(0, pair)
                if len(temp_list) == 1:
                    shuffle()
                continue
            destination = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Names', list_of_names[i] + '.txt')
            with open(destination, "w") as f:
                content = list_of_names[i] + ' gives a gift to: ' + pair
                f.write(content)
            i = i + 1
        list_of_names.clear()
        name_list.delete(0, END)
        info_message.set('Files created..')
        here = os.path.join(tempfile.gettempdir(), 'Secret Santa', 'Names')
        message = 'Christmas Magic has happened..\n\nCheck out the files here:\n\n'
        if 'Desktop' in here:
            desktop = os.getcwd().find('Desktop')
            chop_chop = here[desktop:]
            message += str(chop_chop)
        else:
            message += here
        tk.messagebox.showinfo('Done', message)


def new():
    """
    Clears the inputs
    """
    list_of_names.clear()
    name_list.delete(0, END)


def open_folder():
    """
    Checks if folder exist, if ! then it creates the folder.
    """
    try:
        temp_folder = os.path.join(tempfile.gettempdir(), 'Secret Santa')
        os.startfile(temp_folder)
    except:
        os.makedirs(temp_folder)
        os.startfile(temp_folder)

    
def entry_box(event):
    """
    entry field to get the names
    """
    if text.get() == "Enter the name here...":
        text.delete(0, 'end')
        return None
    else:
        name = str(text.get())
        entry = name.capitalize()
        if get_name(entry):
            name_list.insert(END, entry)
        text.delete(0, 'end')


def remove(x):
    """
    remove names from list
    """
    try:
        x = 0
        selection = name_list.index(ACTIVE)
        target = list_of_names[int(selection)]
        message = target + ' is removed.'
        info_message.set(message)
        del list_of_names[int(selection)]
        name_list.delete(ACTIVE)
    except:
        info_message.set('First, enter a name.')


def mytoggle():
    val = yesno.get()
    if val:
        return 0
    else:
        return 1


def about():
    message = 'Thanks 4 testing!\nGitHUB: pilafxy\nVersion: 1.2'
    tk.messagebox.showinfo('About', message)


def exit():
    if mytoggle()==1:
        info_message.set('Exiting...')
        window.destroy()
        sys.exit(0)    #for command line
        #quit()          #for exe
    else:
        file_path = os.path.join(tempfile.gettempdir(), 'Secret Santa')
        shutil.rmtree(file_path)
        info_message.set('Exiting...')
        window.destroy()
        sys.exit(0)    #for command line
        #quit()          #for exe


"""
GUI
"""
####Frame####
window = Tk()
window.title("Secret Santa Shuffle")
C = Canvas(window, height=400, width=400)
filename = PhotoImage(file=os.path.join(os.getcwd(), "bcgnd.gif"))
background = Label(window, image=filename)
background.place(x=0, y=0, relwidth=1, relheight=1)
welcome_lbl = Label(window, text="Secret Santa Shuffle", bg="white", font=('Christmas', 15))
welcome_lbl.place(x=110, y=5)

####Menu####
menu = Menu(window)
File = Menu(menu, tearoff=0)
File.add_command(label='New', command=new)
File.add_command(label='Open', command=open_folder)
save_menu = Menu(menu, tearoff=0)
save_menu.add_command(label="Slot - 1", command=lambda: save('1'))
save_menu.add_command(label="Slot - 2", command=lambda: save('2'))
save_menu.add_command(label="Slot - 3", command=lambda: save('3'))
File.add_cascade(label='Save', menu=save_menu, underline=0)
load_menu = Menu(menu, tearoff=0)
load_menu.add_command(label="Slot - 1", command=lambda: load('1'))
load_menu.add_command(label="Slot - 2", command=lambda: load('2'))
load_menu.add_command(label="Slot - 3", command=lambda: load('3'))
File.add_cascade(label='Load', menu=load_menu, underline=0)
File.add_separator()
File.add_command(label="Exit", command=exit)

Help = Menu(menu, tearoff=0)
Help.add_command(label="How to use", command=help_me)
yesno = BooleanVar(window)
Help.add_checkbutton(label="Clear Data on close?", variable=yesno, command=mytoggle)
Help.add_command(label="About..", command=about)
menu.add_cascade(label='Menu', menu=File)
menu.add_cascade(label='Help', menu=Help)
window.config(menu=menu)

####Input####
text = Entry(window, bd=4)
text.place(x=60, y=195)
text.insert(0, 'Enter the name here...')
text.bind("<Button-1>", entry_box)
text.bind("<Return>", entry_box)

####Buttons####
btn_get = Button(window, text="Magic", bg="white", font="Christmas, 10", padx=5, pady=5, command=shuffle)
btn_get.place(x=20, y=100)

####Santas Bag#####
labelframe = PanedWindow(window)
labelframe.place(x=245, y=174, heigh=108, width=90)
scrollbar = Scrollbar(labelframe, width=14)
scrollbar.pack(side=RIGHT, fill=Y)
name_list = Listbox(labelframe, bg="#ee1212", fg="white", font=("Arial", 11, "bold"), selectbackground="#c91d28")
name_list.config(yscrollcommand=scrollbar.set)
name_list.bind("<Button-3>", remove)
name_list.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=name_list.yview) #set action for the list box

####Message Bar#####
info_message = StringVar()
info_message.set("Message, info, warning, error will be shown here..")
info_bar = Label(window, textvariable=info_message, relief=GROOVE, bg="white", fg="gray18")
info_bar.place(x=10, y=370, heigh=25, width=385)

check_saves()
C.pack()
window.mainloop()
