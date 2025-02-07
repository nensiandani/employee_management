from customtkinter import *
from PIL import Image
from tkinter import ttk
from tkinter import messagebox
import database

#function
def delete_all():
    if not tree.get_children():
        messagebox.showinfo('Info', 'No records to delete.')
        return

    result = messagebox.askyesno('Confirm', 'Do you really want to delete all the records?')
    if result:
        try:
            # Delete all records from the database
            database.deleteall_records()
            
            # Refresh the Treeview
            treeview_data()
            
            # Notify the user
            messagebox.showinfo('Success', 'All records have been deleted successfully.')
        except Exception as e:
            # Handle any errors
            messagebox.showerror('Error', f'An error occurred: {e}')


def show_all():
    treeview_data()
    searchentry.delete(0,END)
    searchbox.set('Search By')

def search_employee():
    if searchentry.get()=='':
        messagebox.showerror('Eroor','Enter value to search')
    elif searchbox.get()=='Search By':
        messagebox.showerror('Eroor','Please select an option')
    else:
        search_data = database.search(searchbox.get(),searchentry.get())
        tree.delete(*tree.get_children())
        for employee in search_data:
            tree.insert('',END,values=employee)

def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select data to delete')
        return  # Exit the function if no item is selected

    try:
        # Fetch the ID from the selected item in the treeview
        item_id = tree.item(selected_item, 'values')[0]  # Assuming the ID is in the first column
        database.delete(item_id)  # Delete the item from the database
        treeview_data()  # Refresh the treeview to reflect the changes
        clear()  # Clear any associated input fields
         # Display success message
    finally:
        messagebox.showinfo('Success', 'Data has been deleted successfully') 



def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Select data to update')
    else:
        database.update(nameentry.get(),phoneentry.get(),rolebox.get(),genderbox.get(),salaryentry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Data is Updated')

def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        nameentry.insert(0,row[1])
        phoneentry.insert(0,row[2])
        rolebox.set(row[3])
        genderbox.set(row[4])
        salaryentry.insert(0,row[5])


def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    nameentry.delete(0,END)
    phoneentry.delete(0,END)
    rolebox.set('Web Developer')
    genderbox.set('Male')
    salaryentry.delete(0,END)

def treeview_data():
    employees = database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('',END,values=employee)

def add_employee():
    # Auto-generate the ID
    employee_id = database.generate_id()

    if nameentry.get() == '' or phoneentry.get() == '' or salaryentry.get() == '':
        messagebox.showerror('Error', 'All fields are required except ID')
        return
    try:
        database.insert(employee_id, nameentry.get(), phoneentry.get(), rolebox.get(), genderbox.get(), salaryentry.get())
        treeview_data()
        clear()
    finally:
        messagebox.showinfo('Success', f'Employee added successfully with ID {employee_id}!')

def validate_phone_number():
    phone_number = phoneentry.get()
    if not phone_number.isdigit() or len(phone_number) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number")
        phoneentry.delete(0, END)  # Clear the invalid input
        return False
    return True


#GUI parts
window = CTk()
window.title("Employee Management System")
window.geometry("1050x600+100+100")
window.resizable(0, 0)
window.configure(fg_color='Gray')
image = CTkImage(Image.open("D:\python_prog\employee_managment/e2.jpeg"), size=(1050, 200))
imageLabel = CTkLabel(window, image=image, text="")
imageLabel.grid(row=0, column=0,columnspan=2)

leftframe = CTkFrame(window,fg_color='Gray')
leftframe.grid(row=1, column=0)


namelabel = CTkLabel(leftframe,text='Name',font=('arial',18,'bold'),text_color='white')
namelabel.grid(row=1,column=0,padx=20,pady=15,sticky='w')


nameentry = CTkEntry(leftframe,font=('arial',18,'bold'),width=180,bg_color='black',fg_color="white",text_color='black')
nameentry.grid(row=1,column=1)

phonelabel = CTkLabel(leftframe, text='Phone', font=('arial', 18, 'bold'), text_color='white')
phonelabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')

phoneentry = CTkEntry(leftframe, font=('arial', 18, 'bold'), width=180, bg_color='black', fg_color="white", text_color='black')
phoneentry.grid(row=2, column=1, pady=15)

# Bind the validation function to the Phone Entry
phoneentry.bind("<FocusOut>", lambda event: validate_phone_number())


rolelabel = CTkLabel(leftframe,text='Role',font=('arial',18,'bold'),text_color='white')
rolelabel.grid(row=3,column=0,padx=20,pady=15,sticky='w')
role_option = ['Web Developer','Cloud Architect','Network Engineer','DevOps Engineer','Data Scientist','Business Analyst','IT Consultant','UX/UI Designer']
rolebox = CTkComboBox(leftframe,values=role_option,width=180,font=('arial',18,'bold'),bg_color='black',fg_color="white",text_color='black')
rolebox.grid(row=3,column=1,padx=20,pady=15)
rolebox.set('Web Develpoer')

genderlabel = CTkLabel(leftframe,text='Gender',font=('arial',18,'bold'),text_color='white')
genderlabel.grid(row=4,column=0,padx=20,pady=15,sticky='w')


gender_option = ['Male','Female']
genderbox = CTkComboBox(leftframe,values=gender_option,width=180,font=('arial',18,'bold'),bg_color='black',fg_color="white",text_color='black')
genderbox.grid(row=4,column=1,padx=20,pady=15)
genderbox.set('Male')

salarylabel = CTkLabel(leftframe,text='Salary',font=('arial',18,'bold'),text_color='white')
salarylabel.grid(row=5,column=0,padx=20,pady=15,sticky='w')

salaryentry = CTkEntry(leftframe,font=('arial',18,'bold'),width=180,bg_color='black',fg_color="white",text_color='black')
salaryentry.grid(row=5,column=1,pady=15)

rightframe = CTkFrame(window,fg_color='dark gray')
rightframe.grid(row=1, column=1)
search_options = ['Id','Name','Phone','Role','Gender','Salary']
searchbox = CTkComboBox(rightframe,font=('arial',18,'bold'),values=search_options,state='readonly',bg_color='black',fg_color="white",text_color='black')
searchbox.grid(row=0,column=0)
searchbox.set('Search By')

searchentry = CTkEntry(rightframe,font=('arial',18,'bold'),bg_color='black',fg_color="white",text_color='black')
searchentry.grid(row=0,column=1)

searchbutton = CTkButton(rightframe,font=('arial',18,'bold'),text='Search',width=100,command=search_employee)
searchbutton.grid(row=0,column=2)

showallbutton = CTkButton(rightframe,font=('arial',18,'bold'),text='Show All',width=100,command=show_all)
showallbutton.grid(row=0,column=3,pady=4)

tree = ttk.Treeview(rightframe,height=13)
tree.grid(row=1,column=0,columnspan=4)

tree['column'] = ('Id','Name','Phone','Role','Gender','Salary')
tree.heading('Id',text='Id')
tree.heading('Name',text='Name')
tree.heading('Phone',text='Phone')
tree.heading('Role',text='Role')
tree.heading('Gender',text='Gender')
tree.heading('Salary',text='Salary')

tree.config(show='headings')

tree.column('Id',width=100)
tree.column('Name',width=160)
tree.column('Phone',width=160)
tree.column('Role',width=200)
tree.column('Gender',width=100)
tree.column('Salary',width=140)

style = ttk.Style()
style.configure('Treeview.Heading',font=('arial',18,'bold'))
style.configure('Treeview',font=('arial',15,'bold'),rowheight=30,background='white',foreground='black')

scrollbar = ttk.Scrollbar(rightframe,orient=VERTICAL,command=tree.yview)
scrollbar.grid(row=1,column=4,sticky='ns')

tree.config(yscrollcommand=scrollbar.set)

buttonframe = CTkFrame(window,fg_color='Gray')
buttonframe.grid(row=2,column=0,columnspan=2)

newbutton = CTkButton(buttonframe,text='New Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=lambda: clear(True))
newbutton.grid(row=0,column=0,pady=5)

addbutton = CTkButton(buttonframe,text='Add Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=add_employee)
addbutton.grid(row=0,column=1,pady=5,padx=5)

updatebutton = CTkButton(buttonframe,text='Update Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=update_employee)
updatebutton.grid(row=0,column=2,pady=5,padx=5)

deletebutton = CTkButton(buttonframe,text='Delete Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_employee)
deletebutton.grid(row=0,column=3,pady=5,padx=5)

deleteallbutton = CTkButton(buttonframe,text='Delete All',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_all)
deleteallbutton.grid(row=0,column=4,pady=5,padx=5)

treeview_data()

window.bind('<ButtonRelease>',selection)

window.mainloop()
