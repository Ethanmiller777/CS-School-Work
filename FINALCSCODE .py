from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
from SQLloginscreen import dbmanager


class login_manager:
   def __init__(self, master):
       self.master = master
       self.master.geometry("300x200")
       self.master.title("Login/Register Window")
       self.label1 = Label(text="Login/Register", bg="gray55", fg="black", width="300", height="2",
                           font=("Ariel", 13)).pack()
       self.label2 = Label(text="").pack()
       self.button1 = Button(text="Login", bg="gray55", fg="black", width="8", height="1", command=self.login,
                             font=("Ariel", 13)).pack()
       self.label3 = Label(text="").pack()
       self.button2 = Button(text="Register", bg="gray55", fg="black", width="8", height="1", command=self.register,
                             font=("Ariel", 13)).pack()

   def login(self):
       window = Toplevel()  # This creates a blank window on the top
       close_manager_function = self.master.destroy
       login_object = login_screen(window,
                                   close_manager_function)  # Login Object is the window with the buttons(Created by login_screen class)

   def register(self):
       window = Toplevel()  # This creates a blank window on the top
       register_object = register_window(
           window)  # Register Object is the window with the buttons(Created by register window class)


class register_window:
   def __init__(self, master):
       self.master = master
       self.master.title("Register")
       self.master.geometry("300x300")

       self.username = StringVar()
       self.password = StringVar()
       self.info = StringVar()

       Label(master, text="Please Enter your Details Below", bg="gray55", fg="black", width="300", height="2",
             font=("Ariel", 13)).pack()
       Label(master, text="Username * ").pack()
       self.username_entry = Entry(master, textvariable=self.username)
       self.username_entry.pack()
       Label(master, text="Password * ").pack()
       self.password_entry = Entry(master, textvariable=self.password)
       self.password_entry.pack()
       Label(master, text="").pack()
       Button(master, text="Register", bg="gray55", fg="black", width="8", height="1", command=self.register_user,
              font=("Ariel", 13)).pack()
       Label(master, fg="Green", textvariable=self.info).pack()
       Button(master, text="Cancel", bg="gray55", fg="black", width="8", height="1", command=quit,
              font=("Ariel", 13)).pack()

   def register_user(self):
       database = dbmanager(database_name)  # SQLloginscreen is DBManager

       username_info = self.username.get()  # string variable
       password_info = self.password.get()

       result = database.execute(  # Executes the SQL Command
           f"SELECT password FROM Users WHERE Username='{username_info}'")  # checks to make sure that the username has been entered has not already been used
       if len(result) > 0:  # >0 results with matching username
           self.info.set("This information is already in use, try again!")
           self.username_entry.delete(0, END)  # tkinter entry box
           self.password_entry.delete(0, END)
       else:
           database.execute(  # Executes the SQL Command
               f"INSERT INTO Users (Username, Password) VALUES ('{username_info}', '{password_info}')")  # add username and password to the database
           self.info.set("Your Registration was successful")
           self.master.destory()  # Destroys the TopLevel(Closes the register window)


class login_screen:
   def __init__(self, master, close_manager_function):  # passing a function as a parameter
       self.close_manager_function = close_manager_function  # function reference to master.destroy from login_manager
       self.master = master
       self.master.title("Login")
       self.master.geometry("300x250")

       self.username = StringVar()  # A string var is not the same as a string, it is its own class(Mimmicks a string)
       self.password = StringVar()

       Label(master, text="Please Enter your Details Below", bg="gray55", fg="black", width="300", height="2",
             font=("Ariel", 13)).pack()
       Label(master, text="Username * ").pack()
       Entry(master, textvariable=self.username).pack()
       Label(master, text="Password * ").pack()
       Entry(master, textvariable=self.password).pack()
       Label(master, text="").pack()
       Button(master, text="Login", bg="gray55", fg="black", width="8", height="1", command=self.login,
              font=("Ariel", 13)).pack()
       Label(master, text="").pack()
       Button(master, text="Cancel", bg="gray55", fg="black", width="8", height="1", command=master.destroy,
              font=("Ariel", 13)).pack()

   def login(self):
       username = self.username.get()
       password = str(self.password.get())
       database = dbmanager(database_name)
       result = database.execute(
           f"SELECT password FROM Users WHERE Username='{username}'")  # checks that the users entered username and password matches the database
       if len(result) > 0:  # >0 results with matching username
           database_password = str(result[0][0])
           if database_password == password:
               print("Logged in")
               self.master.destroy()
               self.close_manager_function()
               root = Tk()  # this is a window
               my_gui = home_window(root)  # Changes my_gui to home_window as the user has logged in
               root.mainloop()
           else:
               print("Incorrect Password")  # Prints this if the two strings dont match
       else:
           print("Incorrect Details")  # Prints this if the information is totally incorrect


class super_window:
   def __init__(self, master, title="", geometry="1000x1000"):
       self.master = master
       self.master.title(title)
       self.master.geometry(geometry)

   def murderer(self, Message):
       self.master.destroy()
       messagebox.showinfo(title="Info", message=Message)


class home_window(super_window):
   def __init__(self, master: Tcl):
       super().__init__(master, title="Grocery Store Stock Database GUI", geometry="400x300")

       Label(master, font=("Arial", 16, "bold"), bg="gray55", fg="black", width="400", height="2",text="Grocery Store Stock Database").pack()
       Label(text="").pack()
       Button(master, font=("Arial", 13), bg="gray55", fg="black", width="23", height="1",text="View Product Information", command=self.view_confirm).pack()
       Label(text="").pack()
       Button(master, font=("Arial", 13), bg="gray55", fg="black", width="23", height="1",text="Add Product Information", command=self.insert_products).pack()
       Label(text="").pack()
       Button(master, font=("Arial", 13), bg="gray55", fg="black", width="19", height="1", text="Supplier Orders",command=self.supplier_confirm).pack()
       Label(text="").pack()
       Button(master, font=("Arial", 13, "bold"), bg="gray55", fg="black", width="8", height="1", text="QUIT",command=master.destroy).pack()

   def view_confirm(self):
       answer = messagebox.askyesno(title="Confirmation", message="Are you sure you would like to View the Database")
       if answer == YES:
           print("Replace this with link to database later in the future")
       else:
           quit

   def edit_confirm(self):
       answer = messagebox.askyesno(title="Confirmation", message="Are you sure you would like to Edit the Database")
       if answer == YES:
           print("Replace this with link to database later in the future")
       else:
           quit

   def supplier_confirm(self):
       answer = messagebox.askyesno(title="Confirmation", message="Are you sure you would like to view the Database")
       if answer == YES:
           print("Replace this with link to supplier orders later in the future")
       else:
           quit

   def insert_products(self):
       window = Toplevel()
       product_object = add_products(window)

class text_and_entry:
   def __init__(self, master, text, default_text=""):
       self.text_var = StringVar(master, value=default_text)
       Label(master, text=text).pack()
       Entry(master, textvariable=self.text_var).pack()

   def get(self):
       return self.text_var.get()


class add_products(super_window):
   def __init__(self, master):
       super().__init__(master, title="Add Products", geometry="400x400")

       self.productname = text_and_entry(master, "Product Name")
       self.productprice = text_and_entry(master, "Product Price")
       self.productweight = text_and_entry(master, "Product Weight")
       self.producttype = text_and_entry(master, "Product Type")
       self.productstock = text_and_entry(master, "Product Stock")
       Label(master, text="").pack()
       Button(master, font=("Arial", 13, "bold"), bg="gray55", fg="black", width="8", height="1", text="OK",command=self.add).pack()
       Label(master, text="").pack()
       Button(master, font=("Arial", 13, "bold"), bg="gray55", fg="black", width="8", height="1", text="CANCEL",command=master.destroy).pack()

   def add(self):
       name = self.productname.get()
       price = self.productprice.get()
       weight = self.productweight.get()
       p_type = self.producttype.get()
       stock = self.productstock.get()
       database = dbmanager(database_name)
       database.execute(f"""INSERT INTO Product_Information(Product_Name, Product_Price, Product_Weight, Product_Type) VALUES('{name}', {price}, {weight}, '{p_type}')""")
       self.murderer("Your Product has been added to the database, you may close this window")

   #try:
       #command = f"""INSERT INTO Product_Information(Product_Name, Product_Price, Product_Weight, Product_Type)) VALUES('{name}', {price}, {weight}, '{p_type}')"""
  # except sqlite3.OperationalError:
       #messagebox.showerror("ERROR", "You can't do this command")

database_name = "grocerystore_database.db"
LOGIN = None
FILENAME = ""
if __name__ == "__main__":
   login_window = Tk()
   login_gui = login_manager(login_window)
   login_window.mainloop()

