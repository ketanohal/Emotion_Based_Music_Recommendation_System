import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess
from tkinter import messagebox, Tk
from tkinter.font import Font
import subprocess
import sys
import re

root = Tk()
connection = mysql.connector.connect(host='localhost', user='root', port='3306', password='', database='py_lg_rg_db')
c = connection.cursor()

# width and height
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# background color
bgcolor = "#ADD8E6"

# ----------- CENTER FORM ------------- #
root.overrideredirect(1)  # remove border
root.geometry("%dx%d+0+0" % (w, h))
root.state('zoomed')

# ----------- HEADER ------------- #

headerframe = tk.Frame(root, highlightbackground='#6CA6CD', highlightcolor='#6CA6CD', highlightthickness=2,
                       bg='#95a5a6',
                       width=w, height=70)
titleframe = tk.Frame(headerframe, bg='yellow', padx=1, pady=1)
title_label = tk.Label(titleframe, text='Login', padx=20, pady=5, bg='#2980b9', fg='#fff', font=('Tahoma', 24), width=8)
close_button = tk.Button(headerframe, text='x', borderwidth=1, relief='solid', font=('Verdana', 12))

headerframe.pack()
titleframe.pack()
title_label.pack()
close_button.pack()

titleframe.place(y=26, relx=0.5, anchor=CENTER)
close_button.place(x=1506, y=2)


# close window
def close_win():
    root.destroy()


close_button['command'] = close_win

# ----------- END HEADER ------------- #

mainframe = tk.Frame(root, width=w, height=h)


def clear_entry_text(event):
    entry = event.widget
    current_text = entry.get()
    initial_text = entry.initial_text
    if current_text == initial_text:
        entry.delete(0, tk.END)


# ----------- Login Page ------------- #
loginframe = tk.Frame(mainframe, width=w, height=h)
login_contentframe = tk.Frame(loginframe, padx=30, pady=180, highlightbackground='#6CA6CD', highlightcolor='#6CA6CD',
                              highlightthickness=2, bg=bgcolor)

username_label = tk.Label(login_contentframe, text='Username:', font=('Verdana', 16), bg=bgcolor)
password_label = tk.Label(login_contentframe, text='Password:', font=('Verdana', 16), bg=bgcolor)

# Create entry fields
username_entry = tk.Entry(login_contentframe, font=('Verdana', 12), fg='gray', highlightbackground='gray', highlightcolor='gray')
password_entry = tk.Entry(login_contentframe, font=('Verdana', 12), show='*', fg='gray', highlightbackground='gray', highlightcolor='gray')

# Set the initial highlighted text in the entry fields
username_entry.insert(0, 'Enter your username')
username_entry.initial_text = 'Enter your username'

password_entry.insert(0, 'Enter your password')
password_entry.initial_text = 'Enter your password'

# Configure regular and highlighted font styles
regular_font = Font(family='Verdana', size=16)
highlight_font = Font(family='Verdana', size=10)

# Configure initial appearance of entry fields
username_entry.configure(font=highlight_font)
password_entry.configure(font=highlight_font)

# Bind the click event to remove the initial text
username_entry.bind('<Button-1>', clear_entry_text)
password_entry.bind('<Button-1>', clear_entry_text)

login_button = tk.Button(login_contentframe, text="Login", font=('Verdana', 16), bg='#2980b9', fg='#fff', padx=25,
                         pady=10, width=25)

go_register_label = tk.Label(login_contentframe, text="Not a Member ? Click here to Register...", font=('Verdana', 10),
                             bg=bgcolor, fg='red')

mainframe.pack(fill='both', expand=1)
loginframe.pack(fill='both', expand=1)
login_contentframe.place(relx=0.5, rely=0.5, anchor=CENTER)

username_label.grid(row=0, column=0, pady=10, sticky="E")
username_entry.grid(row=0, column=1)

password_label.grid(row=1, column=0, pady=10, sticky="E")
password_entry.grid(row=1, column=1)

login_button.grid(row=2, column=0, columnspan=2, pady=40)

go_register_label.grid(row=3, column=0, columnspan=2, pady=20)


# create a function to display the register frame
def go_to_register():
    loginframe.forget()
    registerframe.pack(fill="both", expand=1)
    title_label['text'] = 'Register'
    title_label['bg'] = '#2980b9'


go_register_label.bind("<Button-1>", lambda page: go_to_register())


# create a function to make the user login
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    vals = (username, password,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s and `password` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        messagebox.showinfo('Login', 'Login successful')
        subprocess.run(['python', 'home.py'])
        root.destroy()  # Close the current running page
    else:
        messagebox.showwarning('Error', 'Wrong username or password')


login_button['command'] = login


# ----------- Register Page ------------- #
def clear_entry_text(event):
    entry = event.widget
    current_text = entry.get()
    initial_text = entry.initial_text
    if current_text == initial_text:
        entry.delete(0, tk.END)


registerframe = tk.Frame(mainframe, width=w, height=h)
register_contentframe = tk.Frame(registerframe, padx=30, pady=180, highlightbackground='#6CA6CD',
                                 highlightcolor='#6CA6CD',
                                 highlightthickness=2, bg=bgcolor)

fullname_label_rg = tk.Label(register_contentframe, text='Fullname:', font=('Verdana', 14), bg=bgcolor)
username_label_rg = tk.Label(register_contentframe, text='Username:', font=('Verdana', 14), bg=bgcolor)
password_label_rg = tk.Label(register_contentframe, text='Password:', font=('Verdana', 14), bg=bgcolor)
confirmpass_label_rg = tk.Label(register_contentframe, text='Re-Password:', font=('Verdana', 14), bg=bgcolor)
phone_label_rg = tk.Label(register_contentframe, text='Phone:', font=('Verdana', 14), bg=bgcolor)
gender_label_rg = tk.Label(register_contentframe, text='Gender:', font=('Verdana', 14), bg=bgcolor)
fullname_entry_rg = tk.Entry(register_contentframe, font=('Verdana', 14), width=22)
username_entry_rg = tk.Entry(register_contentframe, font=('Verdana', 14), width=22)
password_entry_rg = tk.Entry(register_contentframe, font=('Verdana', 14), width=22, show='*')
password_contain_rg = tk.Label(register_contentframe, text="password must contain atleast one captial, one small "
                                                           "Alphabet and one symbol", font=('Verdana', 6), width=66,
                               fg='red')
confirmpass_entry_rg = tk.Entry(register_contentframe, font=('Verdana', 14), width=22, show='*')
phone_entry_rg = tk.Entry(register_contentframe, font=('Verdana', 14), width=22)

# Set the initial highlighted text in the entry fields
fullname_entry_rg.insert(0, 'Eg. Ketan Ohal')
fullname_entry_rg.initial_text = 'Eg. Ketan Ohal'

username_entry_rg.insert(0, 'Eg. Jerry')
username_entry_rg.initial_text = 'Eg. Jerry'

password_entry_rg.insert(0, 'Ketan@123')
password_entry_rg.initial_text = 'Ketan@123'

confirmpass_entry_rg.insert(0, 'Enter same password as above')
confirmpass_entry_rg.initial_text = 'Enter same password as above'

phone_entry_rg.insert(0, 'Eg. 9623061402')
phone_entry_rg.initial_text = 'Eg. 9623061402'

# Configure regular and highlighted font styles
regular_font = Font(family='Verdana', size=12)
highlight_font = Font(family='Verdana', size=10)

# Configure initial appearance of entry fields
fullname_entry_rg.configure(fg='gray', font=highlight_font)
username_entry_rg.configure(fg='gray', font=highlight_font)
password_entry_rg.configure(fg='gray', font=highlight_font)
confirmpass_entry_rg.configure(fg='gray', font=highlight_font)
phone_entry_rg.configure(fg='gray', font=highlight_font)

# Bind the click event to remove the initial text
fullname_entry_rg.bind('<Button-1>', clear_entry_text)
username_entry_rg.bind('<Button-1>', clear_entry_text)
password_entry_rg.bind('<Button-1>', clear_entry_text)
confirmpass_entry_rg.bind('<Button-1>', clear_entry_text)
phone_entry_rg.bind('<Button-1>', clear_entry_text)

radiosframe = tk.Frame(register_contentframe)
gender = StringVar()
gender.set('Male')
male_radiobutton = tk.Radiobutton(radiosframe, text='Male', font=('Verdana', 14), bg=bgcolor, variable=gender,
                                  value='Male')
female_radiobutton = tk.Radiobutton(radiosframe, text='Female', font=('Verdana', 14), bg=bgcolor, variable=gender,
                                    value='Female')

register_button = tk.Button(register_contentframe, text="Register", font=('Verdana', 16), bg='#2980b9', fg='#fff',
                            padx=25, pady=10, width=25)

go_login_label = tk.Label(register_contentframe, text="Already a member ? Click here to sign in...",
                          font=('Verdana', 10),
                          bg=bgcolor, fg='red')

# mainframe.pack(fill='both', expand=1)
# registerframe.pack(fill='both', expand=1)
register_contentframe.place(relx=0.5, rely=0.5, anchor=CENTER)

fullname_label_rg.grid(row=0, column=0, pady=5, sticky='e')
fullname_entry_rg.grid(row=0, column=1)

username_label_rg.grid(row=1, column=0, pady=5, sticky='e')
username_entry_rg.grid(row=1, column=1)

password_label_rg.grid(row=2, column=0, pady=5, sticky='e')
password_entry_rg.grid(row=2, column=1)

password_contain_rg.grid(row=3, column=1, pady=5, sticky='e')

confirmpass_label_rg.grid(row=4, column=0, pady=5, sticky='e')
confirmpass_entry_rg.grid(row=4, column=1)

phone_label_rg.grid(row=5, column=0, pady=5, sticky='e')
phone_entry_rg.grid(row=5, column=1)

gender_label_rg.grid(row=6, column=0, pady=5, sticky='e')
radiosframe.grid(row=6, column=1)
male_radiobutton.grid(row=0, column=0)
female_radiobutton.grid(row=0, column=1)

register_button.grid(row=8, column=0, columnspan=2, pady=20)

go_login_label.grid(row=9, column=0, columnspan=2, pady=10)


# create a function to display the login frame
def go_to_login():
    registerframe.forget()
    loginframe.pack(fill="both", expand=1)
    title_label['text'] = 'Login'
    title_label['bg'] = '#2980b9'


go_login_label.bind("<Button-1>", lambda page: go_to_login())

# --------------------------------------- #
import re


def check_username(username):
    vals = (username,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        return True
    else:
        return False


def register():
    fullname = fullname_entry_rg.get().strip()
    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()
    phone = phone_entry_rg.get().strip()
    gdr = gender.get()

    if len(fullname) == 0 or len(username) == 0 or len(password) == 0 or len(phone) == 0:
        messagebox.showwarning('Empty Fields', 'Please fill in all the required information')
    elif not re.match(r'^[a-zA-Z ]+$', fullname):
        messagebox.showwarning('Invalid Full Name', 'Full name should only contain letters and spaces')
    elif len(password) <= 7:
        messagebox.showwarning('Password', 'Password should be at least 8 characters long')
    elif not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not re.search(
            r'[^\w\s]', password):
        messagebox.showwarning('Password', 'Password must contain at least one uppercase letter, one lowercase '
                                           'letter, and one symbol')
    elif password != confirm_password:
        messagebox.showwarning('Password', 'Passwords do not match')
    elif not phone.isdigit() or len(phone) != 10:
        messagebox.showwarning('Phone', 'Phone number should be a 10-digit number')
    elif not check_username(username):
        vals = (fullname, username, password, phone, gdr)
        insert_query = "INSERT INTO `users`(`fullname`, `username`, `password`, `phone`, `gender`) VALUES (%s,%s,%s," \
                       "%s,%s) "
        c.execute(insert_query, vals)
        connection.commit()
        messagebox.showinfo('Register', 'Your account has been created successfully')
    else:
        messagebox.showwarning('Duplicate Username', 'This username already exists, please choose another one')


register_button['command'] = register

# --------------------------------------- #

# ------------------------------------------------------------------------ #


root.mainloop()
