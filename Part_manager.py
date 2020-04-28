from tkinter import *
from tkinter import messagebox

from db import Database

db = Database('store.db')


def populate_list():
    part_list.delete(0, END)
    for row in db.fetch():
        part_list.insert(END, row)


def add_item():
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required Fields', 'Please Include all Fields')
        return
    db.insert(part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    part_list.delete(0, END)
    part_list.insert(END, (part_text.get(), customer_text.get(), retailer_text.get(), price_text.get()))
    clear_item()
    populate_list()


def select_item(event):
    global selected_item
    try:
        index = part_list.curselection()[0]
        selected_item = part_list.get(index)

        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    populate_list()


def clear_item():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)


# Create window Object
app = Tk()

# PART
part_text = StringVar()
part_label = Label(app, text='Part Name : ', font=('bold', 14), pady=20)
part_label.grid(row=0, column=0, sticky=W)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)
# CUSTOMER
customer_text = StringVar()
customer_label = Label(app, text='Customer  : ', font=('bold', 14))
customer_label.grid(row=0, column=2, sticky=W)
customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)
# RETAILER
retailer_text = StringVar()
retailer_label = Label(app, text='Retailer Name : ', font=('bold', 14))
retailer_label.grid(row=1, column=0, sticky=W)
retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)
# PRICE
price_text = StringVar()
price_label = Label(app, text='Price : ', font=('bold', 14))
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)

# PARTS LISTS
part_list = Listbox(app, height=8, width=70, border=0)
part_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# Create Scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# SET SCROLL TO LIST BOX
part_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=part_list.yview)

# Bind Select
part_list.bind('<<ListboxSelect>>', select_item)

# BUTTON
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Part', width=12, command=clear_item)
clear_btn.grid(row=2, column=3)

app.title("PART MANAGER")
app.geometry('700x350')

# Populate Data
populate_list()

# START PROGRAM
app.mainloop()
