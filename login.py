from customtkinter import *
from PIL import Image
from tkinter import messagebox

def login():
    if username.get()=='' or password.get()=='':
        messagebox.showerror('Error','All the fields requird')
    else:
        messagebox.showinfo('Success', 'Login is successful.')
        root.destroy()
        import ems

# Create the root window
root = CTk()
root.geometry("1050x600")
root.resizable(0, 0)
root.title("Login Page")

# Load and display the image
image = CTkImage(Image.open("D:\python_prog\employee_managment/e1.jpeg"), size=(1050, 600))
imageLabel = CTkLabel(root, image=image, text="")
imageLabel.place(x=0, y=0)  # Correctly place the label on the window

hedinglabel = CTkLabel(root,text="Employee Managemnet System",bg_color='white',text_color='black', font=("Arial", 20, "bold"))
hedinglabel.place(x=20,y=30)

username = CTkEntry(root,placeholder_text='Enter Your UserName',font=('arial',15,'bold'),width=180,bg_color='black',fg_color="white",text_color='black')
username.place(x=30,y=80)

password = CTkEntry(root,placeholder_text='Enter Your Password',font=('arial',15,'bold'),width=180,bg_color='black',fg_color="white",text_color='black',show='*')
password.place(x=30,y=130)

login = CTkButton(root,text='Login',font=('arial',16,'bold'),width=140,cursor='hand2',command=login)
login.place(x=45,y=180)

# Run the application
root.mainloop()
