from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import pandas as pd
from tkinter import Toplevel
from functools import reduce
import random

top = Tk()
top.geometry("370x600")
top.title("nandana")

# name of message creation and placement
p1=Label(top, text="MESSAGE NAME: ")
p1.place(x=20, y=50)
v1 = StringVar()
e1=Entry(top, textvariable=v1)
e1.place(x=140, y=50, width=200)

# message type creation and placement
p2=Label(top, text="MESSAGE TYPE: ")
p2.place(x=20, y=90)
options = ["RT-RT", "RT-BC", "BC-RT"]
clicked = StringVar()
clicked.set("Select option")
drop=OptionMenu(top, clicked, *options)
drop.place(x=140, y=90, width=200)

# no of words creation and placement
p3=Label(top, text="NO. OF WORDS: ")
p3.place(x=20, y=130)
v3 = IntVar()
v3.set('')
e3=Entry(top, textvariable=v3)
e3.place(x=140, y=130, width=200)

# frequency creation and placement
p4=Label(top, text="FREQ(in ms): ")
p4.place(x=20, y=170)
v4 = IntVar()
v4.set('')
e4=Entry(top, textvariable=v4)
e4.place(x=140, y=170, width=200)

#create table
columns = ("MSG NAME", "MSG TYPE", "NO. OF WORDS", "FREQ")
global table
table = ttk.Treeview(top, columns=columns, show='headings')
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=92)
table.place(x=0, y=325, width=370, height=270)

#function to add data to table
def add():
    global selected_item
    pt1 = v1.get()
    pt2 = clicked.get()
    pt3 = v3.get()
    pt4 = v4.get()


    if pt1 and pt2 and pt3 and pt4:
        if pt3>32 or pt3<1:
             messagebox.showwarning("Warning", "NO. OF WORDS should be between 0 and 31")
             return
        if selected_item:
            table.item(selected_item[0], values=(pt1, pt2, pt3, pt4))
            selected_item = None
        else:
            table.insert('', 'end', values=(pt1, pt2, pt3, pt4))

        v1.set('')
        clicked.set("Select option")
        v3.set('')
        v4.set('')

submit=Button(top, text="SUBMIT", command=add, fg="purple")
submit.place(x=150, y=200)

selected_item = None

#menu
def menu(event):
    global selected_item
    selected_item = table.selection()
    if selected_item:
        menu = Menu(top, tearoff=0)
        menu.add_command(label="Edit", command=edit_row)
        menu.add_command(label="Delete", command=lambda: delete_row(selected_item))
        menu.post(event.x_root, event.y_root)

#function to delete
def delete_row(item):
    global selected_item
    for i in item:
        table.delete(i)
    selected_item = None
    messagebox.showinfo("Deleted", "Row deleted successfully")

#function to edit
def edit_row():
    global selected_item
    if selected_item:
        item = selected_item[0]
        values = table.item(item, 'values')
        v1.set(values[0])
        clicked.set(values[1])
        v3.set(values[2])
        v4.set(values[3])

table.bind("<Button-3>", menu)

def export_to_excel():
    # Open a file dialog to ask for the save location and filename
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        title="Save as"
    )

    # Check if the user did not cancel the dialog
    if file_path:
        try:
            # Collect data from the table
            rows = [table.item(item)['values'] for item in table.get_children()]
            df = pd.DataFrame(rows, columns=columns)
            
            # Save the data to the selected file
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Exported", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

ip_export=Button(top, text="EXPORT TO EXCEL", command=export_to_excel, fg="purple")
ip_export.place(x=120, y=230)

def import_from_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                table.insert('', 'end', values=(row['MSG NAME'], row['MSG TYPE'], row['NO. OF WORDS'], row['FREQ']))
            messagebox.showinfo("Imported", f"Data imported from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {e}")

import_ip=Button(top, text="IMPORT FROM EXCEL", command=import_from_excel, fg="purple")
import_ip.place(x=110, y=260)

# to generate cyclogram
def cyclogram():
    global table
    global items
    items = table.get_children()
    if items:
        global msg_freq_list
        msg_freq_list = [(table.item(item)['values'][0],int(table.item(item)['values'][2]),int(table.item(item)['values'][3])) for item in items]
        msg_freq_list.sort(key=lambda x: x[2])

        # Extract messages and frequencies into separate lists
        messages=[]
        global frequencies
        frequencies=[]
        no_of_words=[]

        for msg,word,freq in msg_freq_list:
            messages.append(msg)
            no_of_words.append(word)
            frequencies.append(freq)
        global mi
        mi=frequencies[0]
        ma=frequencies[-1]
        global n
        n=ma//mi

        global cg
        cg = Toplevel(top)
        cg.title("Cyclogram nandana")
        
        global total_width
        total_width = 600  # base width
        if n>0:
            total_width = int(75*n)
        
        min_width = 400
        total_width = max(min_width, int(75 * n))
        cg.geometry(f"{total_width}x600")

        heading = Label(cg, text="CYCLOGRAM WITH SLOT LOADS FOR EACH COLUMN")
        heading.place(x=0.02 * total_width, y=10, anchor="w")

        global l
        l=[str(x) for x in range(1,n+1)]

        global cyclo
        cyclo = ttk.Treeview(cg, columns=l, show='headings')
        for col in l:
            cyclo.heading(col, text=str(col))
            cyclo.column(col, width=total_width//n)
        cyclo.place(x=0, y=70, width=total_width, height=500)

        global slots
        slots = [["" for _ in range(n)] for _ in range(len(items))]
        
        # Populate the slots based on frequencies
        for i,freq in enumerate(frequencies):
            msg_name = messages[i]
            step = max(freq//mi,1)
            for j in range(0, n, step):
                slots[i][j]=msg_name
        
        # Insert slots into the Treeview
        for col_values in slots:
            cyclo.insert('', 'end', values=col_values)
        
        empty=[""]*n 
        loads=["LOADS:"]+[""]*n 
        cyclo.insert('', 'end', values=empty)
        cyclo.insert('', 'end', values=loads)
        cyclo.insert('', 'end', values=empty)

        slot_load_percentages,overall_load=load()
        
        # Ensure the slot load percentages match the number of columns
        slot_load_percentages = [f"{load:.2f}%" for load in slot_load_percentages]
        if len(slot_load_percentages) < n:
            slot_load_percentages.extend([""] * (n - len(slot_load_percentages)))
        
        cyclo.insert('', 'end', values=slot_load_percentages)
        
        ol=Label(cg,text="OVERALL LOAD: ")
        ol.place(x=10,y=40)
        
        global olv
        olv=Label(cg,text=f"{overall_load:.2f}%")
        olv.place(x=150,y=40)

            
        cyclo_export=Button(cg, text="EXPORT TO EXCEL", command=export_cyclogram, fg="blue")
        cyclo_export.place(x=total_width-230, y=40)

        evend=Button(cg, text="EVEN DISTR", command=even_distribution, fg="blue")
        evend.place(x=total_width-230, y=15)

def load():
    
    cyclo_rows=[cyclo.item(item)['values'] for item in cyclo.get_children()]
    messages_by_column = {col:[] for col in range(n)}

    for row in cyclo_rows:
        for col,msg in enumerate(row):
            if msg:
                messages_by_column[col].append(msg)

    message_words = {}
    for name,no_words,_ in msg_freq_list:
        message_words[name]=no_words

    time_per_word = 20          # one word -> 20 bits
    slot_duration = mi*1000     # converting mi to microseconds

    time_used = [0] * n 
    for col, msgs in messages_by_column.items():
        for msg in msgs:
            if msg in message_words:
                time_used[col]=time_used[col]+(message_words[msg]*time_per_word)

    slot_loads=[(load/slot_duration)*100 for load in time_used]
    overall_load=((reduce(lambda x,y: x+y,time_used))/(slot_duration*n))*100

    return slot_loads,overall_load

def even_distr():
    global slots
    max_columns = len(slots[0])
    total_rows = len(slots)
    
    def get_message_positions(row):
        positions = {}
        for idx, val in enumerate(row):
            if val != '':
                if val not in positions:
                    positions[val] = []
                positions[val].append(idx)
        return positions
    
    def can_place_message(row, message_positions, start_index):
        for msg, positions in message_positions.items():
            for idx in positions:
                if start_index + idx >= len(row) or row[start_index + idx] != '':
                    return False
        return True

    def place_message(row, message_positions, start_index):
        for msg, positions in message_positions.items():
            for idx in positions:
                row[start_index + idx] = msg

    def clear_message(row, message_positions):
        for msg, positions in message_positions.items():
            for idx in positions:
                row[idx] = ''

    # To keep track of the rows that have been merged
    merged = [False] * total_rows

    for current_row in range(total_rows):
        if merged[current_row]:
            continue
        
        current_message_positions = get_message_positions(slots[current_row])
        
        for target_row in range(current_row):
            for start_col in range(max_columns - len(current_message_positions) + 1):
                if can_place_message(slots[target_row], current_message_positions, start_col):
                    # Check if placing messages exceeds load limit
                    new_row = slots[target_row][:]  # Make a copy of the target row
                    place_message(new_row, current_message_positions, start_col)
                    
                    sl,ol=load()
                    if any(sl)>40:
                        continue
                    
                    # If load is acceptable, place message and clear the current row
                    slots[target_row] = new_row
                    clear_message(slots[current_row], current_message_positions)
                    merged[current_row] = True
                    break
            else:
                continue
            break

    # Remove empty rows and compact the list
    slots = [row for row in slots if any(cell != '' for cell in row)]

def even_distribution():
    even_distr()
    
    # Clear existing rows in cyclo
    for item in cyclo.get_children():
        cyclo.delete(item)

    # Insert updated slots into the Treeview
    for col_values in slots:
        cyclo.insert('', 'end', values=col_values)
    
    empty=[""]*n 
    loads=["LOADS:"]+[""]*n 
    cyclo.insert('', 'end', values=empty)
    cyclo.insert('', 'end', values=loads)
    cyclo.insert('', 'end', values=empty)

    slot_load_percentages,overall_load = load()

    # Ensure the slot load percentages match the number of columns
    slot_load_percentages = [f"{load:.2f}%" for load in slot_load_percentages]
    if len(slot_load_percentages) < n:
        slot_load_percentages.extend([""] * (n - len(slot_load_percentages)))
    
    cyclo.insert('', 'end', values=slot_load_percentages)

def export_cyclogram():
    # Open a file dialog to ask for the save location and filename
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        title="Save as"
    )

    # Check if the user did not cancel the dialog
    if file_path:
        try:
            # Collect data from the cyclogram table
            rows = [cyclo.item(item)['values'] for item in cyclo.get_children()]
            df = pd.DataFrame(rows, columns=l)
            
            # Save the data to the selected file
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Exported", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

gen_cyclo=Button(top, text="GENERATE CYCLOGRAM", command=cyclogram, fg="red")
gen_cyclo.place(x=100, y=290)

def test(num_messages):
    global table
    # Clear existing rows
    for item in table.get_children():
        table.delete(item)

    for i in range(1, num_messages + 1):
        msg_name = f"MSG{i}"
        msg_type = random.choice(options)
        freq = [20, 40, 80, 160, 320]
        msg_freq = random.choice(freq)
        no_of_words = random.randint(1, 32)

        v1.set(msg_name)
        clicked.set(msg_type)
        v3.set(no_of_words)
        v4.set(msg_freq)

        add()
        
        # Optional: Add a short delay to see the messages being added if needed
        # time.sleep(0.1)

def rand():
    rand=Toplevel(top)
    rand.title("test cases")

    rand.geometry("220x150")

    val=Label(rand,text="How many test cases: ")
    val.place(x=10,y=10)
    v=IntVar()
    e=Entry(rand,textvariable=v)
    v.set('')
    e.place(x=10,y=30)
    
    def submit_rand():
        num=v.get()
        test(num)
        rand.destroy()

    sub_rand=Button(rand, text="SUBMIT", command=submit_rand, fg="blue")
    sub_rand.place(x=10, y=60)

rand=Button(top, text="RANDOM TEST CASES", command=rand, fg="purple")
rand.place(x=110, y=5)

top.mainloop()