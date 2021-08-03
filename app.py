#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
from tkinter import *
import pymysql

conn = pymysql.connect(
    host="localhost", user="root", password="master123", database="secret_base"
)
cursor = conn.cursor()


def updates(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert("", "end", values=i)
    conn.commit()


def search():
    q2 = q.get().capitalize()
    myquery = f"SELECT *FROM persons WHERE first_name='{q2}' or last_name='{q2}';"
    cursor.execute(myquery)
    thisrows = cursor.fetchall()
    updates(thisrows)


def resetcommand():
    query = "SELECT *FROM persons"
    cursor.execute(query)
    rows = cursor.fetchall()
    updates(rows)


def insert():
    userid = t1.get()
    fname = t2.get()
    lname = t3.get()
    emailid = t4.get()
    query = f"INSERT INTO persons VALUES({userid},'{fname}','{lname}','{emailid}');"

    try:
        cursor.execute(query)
        cursor.execute("SELECT *FROM persons;")
        entries = cursor.fetchall()
        conn.commit()
        ms.showinfo("Added", f"Added to Database,Total entry {len(entries)}")
        resetcommand()
    except Exception as e:
        ms.showinfo("Error", e)
    resetcommand()


def update():
    userid = t1.get()
    fname = t2.get()
    lname = t3.get()
    emailid = t4.get()
    updatequery = f"UPDATE persons SET first_name='{fname}',last_name='{lname}',email='{emailid}' WHERE id ={int(userid)}"

    if ms.askyesno("Confirm Update", "Are you sure?"):
        cursor.execute(updatequery)
        conn.commit()
        resetcommand()
    else:
        return True


def delete():

    delquery = f"DELETE FROM persons WHERE id ={t1.get()}"

    if ms.askyesno("Confirm Delete", "Are you sure?"):
        cursor.execute(delquery)
        conn.commit()
        resetcommand()
    else:
        return True


def getrow(event):
    rowid = trv.identify_row(event.y)
    items = trv.item(trv.focus())
    t1.set(items["values"][0])
    t2.set(items["values"][1])
    t3.set(items["values"][2])
    t4.set(items["values"][3])


root = Tk()
root.title("Personal Database")
root.geometry("850x750")
root.config(bg="#a4a6a6")

# texvariables
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()

# label frames
labelTree = LabelFrame(root, text="Peoples List", bg="#a4a6a6", fg="#2f3232")
searchlabelFrame = LabelFrame(root, text="Search", bg="#a4a6a6", fg="#2f3232")
entrylabelFrame = LabelFrame(root, text="Peoples Data", bg="#a4a6a6", fg="#2f3232")

# label frames setup
labelTree.pack(fill="both", expand="yes", padx=20, pady=20)
searchlabelFrame.pack(fill="both", expand="yes", padx=20, pady=20)
entrylabelFrame.pack(fill="both", expand="yes", padx=20, pady=20)


# initializing treeview
trv = ttk.Treeview(labelTree, columns=(1, 2, 3, 4), show="headings", height=12)
trv.pack()

# customizing heading
trv.heading(1, text="Id Number")
trv.heading(2, text="First Name")
trv.heading(3, text="Last Name")
trv.heading(4, text="Email")

# adding event listner to treeview
trv.bind("<Double 1>", getrow)


# customer list section
query = "select *from persons"
cursor.execute(query)
rows = cursor.fetchall()
updates(rows)


# customer search section
searchBox = Entry(searchlabelFrame, width=45, textvariable=q, bg="white", fg="black")
seachButton = Button(searchlabelFrame, text="Search", command=search)
resetButton = Button(searchlabelFrame, text="Reset", command=resetcommand)

# Search sectiion set up
searchBox.pack(side=LEFT, padx=5)
seachButton.pack(side=LEFT, padx=20)
resetButton.pack(side=LEFT, padx=20)

# user data section
lbl1 = Label(entrylabelFrame, text="Id:", bg="#a4a6a6", fg="#2f3232")
lbl1.grid(row=0, column=0, padx=5, pady=5)

lbl2 = Label(entrylabelFrame, text="First Name:", bg="#a4a6a6", fg="#2f3232")
lbl2.grid(row=1, column=0, padx=5, pady=5)

lbl3 = Label(entrylabelFrame, text="Last Name:", bg="#a4a6a6", fg="#2f3232")
lbl3.grid(row=2, column=0, padx=5, pady=5)

lbl4 = Label(entrylabelFrame, text="Email:", bg="#a4a6a6", fg="#2f3232")
lbl4.grid(row=3, column=0, padx=5, pady=5)


# all entrys
lbl1entry = Entry(entrylabelFrame, bg="white", fg="black", width=50, textvariable=t1)
lbl1entry.grid(row=0, column=1, padx=5, pady=5)

lbl2entry = Entry(entrylabelFrame, bg="white", fg="black", width=50, textvariable=t2)
lbl2entry.grid(row=1, column=1, padx=5, pady=5)

lbl3entry = Entry(entrylabelFrame, bg="white", fg="black", width=50, textvariable=t3)
lbl3entry.grid(row=2, column=1, padx=5, pady=5)

lbl4entry = Entry(entrylabelFrame, bg="white", fg="black", width=50, textvariable=t4)
lbl4entry.grid(row=3, column=1, padx=5, pady=5)

# all enrty buttons
addBtn = Button(entrylabelFrame, text="ADD", bg="white", fg="black", command=insert)
addBtn.grid(row=4, column=0, padx=5, pady=5)

updateBtn = Button(
    entrylabelFrame, text="Update", bg="white", fg="black", command=update
)
updateBtn.grid(row=4, column=1, pady=5)

deleteBtn = Button(
    entrylabelFrame, text="Delete", bg="white", fg="black", command=delete
)
deleteBtn.grid(row=4, column=2, pady=5)


# exit keybinding
root.bind("<Escape>", lambda x: root.destroy())
root.mainloop()
