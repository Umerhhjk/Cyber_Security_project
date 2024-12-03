#pip install email-validator (install this if you havent already)
import tkinter

from email_validator import EmailNotValidError, validate_email

from Filing_logic import *
from Transaction_GUI import Recieve_Money, Send_Money, go_back

X_cord=600   #these represent where to show window on screen
Y_cord=130

#styles --------------------------------------------------
Main_Heading_font= ("Chiller", 45, "bold")
Sub_Headings_font= ("Arial Black", 17, "bold")
Other_Headings_font= ("Arial Black", 30, "bold")
Simple_text_font= ("Arial", 15, "bold")
Button_font1=("Arial Black", 20, "bold")
Button_font2=("Arial Black", 15, "bold")
Entry_label_font=("Arial", 15)
Data_Display_font=("Arial", 10,"bold")
Other_labels_font=("Arial", 15, "bold")

Basic_Button_style = {
    "fg": "white",
    "relief": "raised",
    "borderwidth": 10,
    "activebackground":"white",  # Hover background color
    "activeforeground":"black"  # Hover text color
}

Button_style_1 = {
    "font": Button_font1,
    "width": 10,
    "height": 1,
}

Button_style_2 = {
    "font": Button_font2,
    "width": 10,
    "height": 2,
}

Button_style_3 = {
    "font": Button_font2,
    "width": 20,
    "height": 2,
}

#styles END --------------------------------------------------

#------------------------------------------- Change_Password Functions Start -----------------------------------------

def Validate_Passwod_data(Entered_data,This_username):
    Old_Password,entered_password,entered_confirm_password=Entered_data

    def Validade_new_Password():
        Validation_error=None
        if(entered_password=="" or Old_Password=="" or entered_confirm_password==""):
            Validation_error="Password Fill all input fields." 
        elif(len(entered_password)<8):
            Validation_error="Password should be atleast 8 characters long." 
        if(len(entered_password)<8):
            Validation_error="Password should be atleast 8 characters long." 
        elif(entered_password!=entered_confirm_password):
            Validation_error="Password and Confirm Password fields do not match."
        elif(entered_password==Old_Password):
            Validation_error="New Password can not be the same as old password."
        elif(len(entered_password)>20):
            Validation_error="Password should be atmost 20 characters long."
        elif any(character in entered_password for character in ['#', '"', '\'','\n','!',':']):
            Validation_error="Password contains invalid characters."
        return Validation_error 

    NewPasswordError= Validade_new_Password()
    if(NewPasswordError == None):
       Old_Password_check=check_old_password(This_username,Old_Password)
       if(Old_Password_check!=1):
           return "Invalid Password."
       
    elif(NewPasswordError != None):
        return NewPasswordError

    else:
        return ""

def Change_Password(This_username):
    Change_Password_window = tkinter.Tk()
    Change_Password_window.title("Change Password") 
    Change_Password_window.geometry(f"610x590+{X_cord}+{Y_cord}") 
    Change_Password_window.config(bg="black")

    ID_label=tkinter.Label(Change_Password_window,font=Other_Headings_font, bg="black", fg="#D8a616" ,text="Change Password") 
    ID_label.grid(row=0,column=0,pady=(20,30))

    Change_password_frame=tkinter.LabelFrame(Change_Password_window) 
    Change_password_frame.grid(row=1,column=0 ,padx=20,pady=10)

    Button_Frame=tkinter.LabelFrame(Change_Password_window,bg="black",  relief="flat") 
    Button_Frame.grid(row=5,column=0 ,padx=20,pady=10)

    Old_password_label=tkinter.Label(Change_password_frame,font=Other_labels_font,text="Old Password")   #(this is one of the contained labels)
    Old_password_label.grid(row=1,column=0, pady=10, ipady=5)

    Old_password_entry=tkinter.Entry(Change_password_frame,font=Entry_label_font, bg="white",fg="gray", width=35,show="*")
    Old_password_entry.grid(row=1,column=1, padx=10, pady=10, ipady=5,ipadx=5)

    New_Password=tkinter.Label(Change_password_frame,font=Other_labels_font,text="New Password")
    New_Password.grid(row=2,column=0, pady=10, ipady=5)

    New_Password_entry=tkinter.Entry(Change_password_frame,font=Entry_label_font, bg="white",fg="gray", width=35,show="*")
    New_Password_entry.grid(row=2,column=1, padx=10, pady=10, ipady=5)

    Confirm_New_Password=tkinter.Label(Change_password_frame,font=Other_labels_font,text="Confirm\nNew Password")
    Confirm_New_Password.grid(row=3,column=0, pady=10, ipady=5)

    Confirm_New_Password_entry=tkinter.Entry(Change_password_frame,font=Entry_label_font, bg="white",fg="gray", width=35,show="*")
    Confirm_New_Password_entry.grid(row=3,column=1, padx=10, pady=10, ipady=5)


    Error_label=tkinter.Label(Change_password_frame,font=Simple_text_font, fg="Red",justify="left",text="")  
    Error_label.grid(row=4,column=0, columnspan=2,pady=(10,20))  

    back_button = tkinter.Button(Button_Frame, bg="#901111", text="Cancel",command=lambda: go_back(Change_Password_window),**Button_style_2,**Basic_Button_style)
    back_button.grid(row=5,column=0, padx=20, pady=(20,10)) 

    def Submit_Change_Passwod_data():
        Entered_data = [
            Old_password_entry.get(),  
            New_Password_entry.get(),
            Confirm_New_Password_entry.get(), 
        ]
        error_text=Validate_Passwod_data(Entered_data,This_username)
        Error_label.config(text=error_text)   #if there is an error, display it
        if(error_text=="" or error_text==None):
            Change_Password_window.destroy()
            print("Password Change Successful")
            Update_Password(This_username,Entered_data[1]) 

    Submit_Data_button = tkinter.Button(Button_Frame, bg="#13780a" , text="Submit\nData",command=Submit_Change_Passwod_data, **Button_style_2,**Basic_Button_style)
    Submit_Data_button.grid(row=5,column=1,padx=20,pady=(20,10)) 

#------------------------------------------- Change_Password Functions END -------------------------------------------


#Auxiliary Functions --------------------------------------------------------------------------------
def login_to_Sign_up(login_Window):
    login_Window.destroy()
    Sign_Up_Function()


def Sign_up_to_login(Signup_Window):
    Signup_Window.destroy()
    Login_Function()

def main_to_Sign_up(MainWindow):
    MainWindow.destroy()
    Sign_Up_Function()

def main_to_login(MainWindow):
    MainWindow.destroy()
    Login_Function()

def Log_out(Account_Window):
    Account_Window.destroy()
    Login_Function()    

def Create_User_Account(Singup_data):
    ID=Create_Account(Singup_data)
    Show_User_Account(ID)

def Wrap_over_newline(mystring, limit=20): #this function makes sure the errors are wrapped with the frame, and dont overflow
    words = mystring.split() 
    current_length = 0
    result = []
    for word in words:
        # If adding this word would exceed the limit, insert a newline
        if current_length + len(word) > limit:
            result.append('\n')
            current_length = 0 
        result.append(word) 
        current_length += len(word) + 1  # accounting the space after the word

    return ' '.join(result)  #rejoin with spaces

#Auxiliary Functions END --------------------------------------------------------------------------------------------


#Admin Window --------------------------------------------------------------------------------------------------------
def Show_Admin_Account():
    Admin_Account_Window = tkinter.Tk()
    Admin_Account_Window.title("Admin Account") 
    Admin_Account_Window.geometry(f"465x350+{X_cord}+{Y_cord}") 
    Admin_Account_Window.config(bg="black")


#User_Account Label
    ID_label=tkinter.Label(Admin_Account_Window,font=Main_Heading_font, bg="black", fg="white" ,text="Welcome Admin") 
    ID_label.grid(row=0,column=0,pady=(20,30))

    Admin_frame=tkinter.LabelFrame(Admin_Account_Window,bg="black",  relief="flat") #relief="flat" sets visible boderwidth to 0
    Admin_frame.grid(row=1,column=0 ,padx=20,pady=10)

    Display_All_button = tkinter.Button(Admin_frame, bg="#15aacb" , text="Display\nUser Info",command=Display_All_Users_Info, **Button_style_2,**Basic_Button_style)
    Display_All_button.grid(row=1,column=0,padx=25,pady=(20,10)) 

    Log_out_button = tkinter.Button(Admin_frame, bg="#901111", text="Log out",command=lambda: Log_out(Admin_Account_Window),**Button_style_2,**Basic_Button_style)
    Log_out_button.grid(row=1,column=1,padx=20,pady=(20,10))

def Display_All_Users_Info():
    Display_File_Window = tkinter.Tk()
    Display_File_Window.title("User Info")

   
    txt_data = get_txt_file_data() 

    frame = tkinter.Frame(Display_File_Window)
    frame.pack(fill=tkinter.BOTH, expand=True)

    text_widget = tkinter.Text(frame, wrap=tkinter.WORD, font=('Arial', 10), fg="black")
    text_widget.insert(tkinter.END, txt_data)  
    text_widget.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    scrollbar = tkinter.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    Display_File_Window.mainloop() 

#--------------------------------- Admin WIndow ENDS -------------------------------------------------------------------


#User Window --------------------------------------------------------------------------------------------------------
def Show_User_Account(Acount_Id):
    # Creating the main window
    User_Account_Window = tkinter.Tk()
    User_Account_Window.title("User Account")
    User_Account_Window.geometry(f"465x475+{X_cord}+{Y_cord}")  
    User_Account_Window.config(bg="black")

    Account_Details=get_Details(str(Acount_Id)) # found in filing_logic.cpp

    Username,Email,Account_Balance,Password,Public_Key,Private_Key,Acount_Id=Account_Details

    balance_text="(Account Balance: " + Account_Balance + " Rs)"

#User_Account Label
    ID_label=tkinter.Label(User_Account_Window,font=Main_Heading_font, bg="black", fg="white" ,text=Username) 
    ID_label.grid(row=0,column=0,pady=(15,15))

    Balance_label=tkinter.Label(User_Account_Window,font=Sub_Headings_font, bg="black", fg="white" ,text=balance_text) 
    Balance_label.grid(row=1,column=0,pady=(30,10))

    user_frame=tkinter.LabelFrame(User_Account_Window,bg="black",  relief="flat") #relief="flat" sets visible boderwidth to 0
    user_frame.grid(row=2,column=0 ,padx=20,pady=10)

    Send_Money_button = tkinter.Button(user_frame, bg="#15aacb" , text="Send\nMoney",command=lambda: Send_Money(Account_Balance,Username,Balance_label,Account_Balance), **Button_style_2,**Basic_Button_style)
    Send_Money_button.grid(row=2,column=0,padx=25,pady=(20,10)) 

    Recieve_Money_button = tkinter.Button(user_frame, bg="#13780a" , text="Recieve\nMoney",command=lambda: Recieve_Money(Username,Balance_label,Account_Balance), **Button_style_2,**Basic_Button_style)
    Recieve_Money_button.grid(row=2,column=1,padx=20,pady=(20,10)) 

    Change_Password_button = tkinter.Button(user_frame, bg="#D8a616" , text="Change\nPassword",command=lambda: Change_Password(Username), **Button_style_2,**Basic_Button_style)
    Change_Password_button.grid(row=3,column=0,padx=20,pady=(20,10)) 

    Log_out_button = tkinter.Button(user_frame, bg="#901111", text="Log out",command=lambda: Log_out(User_Account_Window),**Button_style_2,**Basic_Button_style)
    Log_out_button.grid(row=3,column=1,padx=20,pady=(20,10)) 
#User Window ENDS --------------------------------------------------------------------------------------------------------

# Functions to remove or Add Placeholder text --------------------------------------------------
def on_focus_in(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tkinter.END)  # Remove the placeholder text
        entry.config(fg="black")  # Change text color to black when typing
        if(placeholder_text=="Password" or placeholder_text=="Confirm Password"):
            entry.config(show="*")  #if user is entering a password, show * instead of actual letters


def on_focus_out(event, entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")  # Placeholder text color set back to gray
        if(placeholder_text=="Password" or placeholder_text=="Confirm Password"):
            entry.config(show="") # (in case of password) when nothing in field, show the placeholder instead of '*' 

#----------------------------------------------------------------------------------------------------


#Login/Signup data Validation ------------------------------------------------------------------------------------------
def Validate_Signup_data(Singup_data):
    entered_username, entered_email, entered_password, entered_confirm_password = Singup_data

    All_Usernames = get_All_Usernames() #extract all usernames that currently exist in file

    def Validade_Username():
        Validation_error=None
        if(entered_username=="Username"):
            Validation_error="Please Enter a Username." 
        elif(len(entered_username)<8):
            Validation_error="Username should be atleast 8 characters long." 
        elif(len(entered_username)>20):
            Validation_error="Username should be atmost 20 characters long."    
        elif(entered_username in All_Usernames):
                Validation_error="Username already in use. Choose a different Username."
        elif(' ' in entered_username):
                Validation_error="Username can not contain any spaces."
        elif(entered_username[0].isdigit()):
                Validation_error="Username can not start with a digit."
        elif any(character in entered_username for character in ['#', '"', '\'','\n','!',':','{','}']):
            Validation_error="Username contains invalid characters."
        return Validation_error    

    def Validade_Password():
        Validation_error=None
        if(entered_password!=entered_confirm_password):
            Validation_error="Password and Confirm Password fields do not match."
        elif(len(entered_password)<8):
            Validation_error="Password should be atleast 8 characters long." 
        elif(len(entered_password)>20):
            Validation_error="Password should be atmost 20 characters long."
        elif any(character in entered_password for character in ['#', '"', '\'','\n','!',':']):
            Validation_error="Password contains invalid characters."
        return Validation_error    

    def Validade_Email():
        Validation_error=None
        try:                               # This will validate the email format
          validate_email(entered_email)
          return None   
        except EmailNotValidError as e:
          Validation_error=(str(e))
        return Validation_error

    UsernameError=Validade_Username()
    PasswordError=Validade_Password()
    EmailError=Validade_Email()
    
    ErrorList=[UsernameError,PasswordError,EmailError]
    return ErrorList

def Validate_login_data(login_data):
    Account_Id=Check_In_File(login_data)      #function found in filing_logic.py it returns an id if account is found in file, otherwise returns "0"

    Result=[None,0]   #if account is found, we need the id, else we need to print an error, index 0 is error, index 1 is id
    if(Account_Id=="0"):
       Result[0]="Username or Password Is incorrect."
    else:   
        Result[1]=int(Account_Id)
     
    return Result

#----------------------------------- Login/Signup data Validation ENDS -------------------------------------------------------


# --------------------------- Sign Up window ---------------------------------------------------------------------------
def Sign_Up_Function():

   Signup_Window = tkinter.Tk()
   Signup_Window.title("Signup Window")  # Title forSignup_Window
   Signup_Window.geometry(f"465x550+{X_cord}+{Y_cord}")  # Size forSignup_Window
   Signup_Window.config(bg="black")  # Set background color ofSignup_Window

   name_placeholder = "Username"
   password_placeholder = "Password"
   Confirm_placeholder = "Confirm Password"
   email_placeholder = "Email"

   Welcomelabel=tkinter.Label(Signup_Window,font=Other_Headings_font, bg="black", fg="Red" ,text="Sign up") 
   Welcomelabel.grid(pady=(10,10))
   
   user_input_frame=tkinter.LabelFrame(Signup_Window)
   user_input_frame.grid(row=1,column=0 ,padx=20,pady=10)

   name_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   name_entry.grid(row=1,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   name_entry.insert(0, name_placeholder)

   email_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   email_entry.grid(row=2,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   email_entry.insert(0, email_placeholder)

   Password_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   Password_entry.grid(row=3,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   Password_entry.insert(0, password_placeholder)

   Confirm_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   Confirm_entry.grid(row=4,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   Confirm_entry.insert(0, Confirm_placeholder)

   # when the user clicks on the submit button, this field becomes visible and displays errors (if any)
   Error_label=tkinter.Label(user_input_frame,font=Simple_text_font, fg="Red",justify="left",text="")  
   Error_label.grid(row=5,column=0,pady=(10,10))    

   def Submit_Singup_data():      #nested functiion to get field values and display possible errors
                          
        Singup_data = [
            name_entry.get(),  
            email_entry.get(), 
            Password_entry.get(),
            Confirm_entry.get()  
        ]

        Problems=Validate_Signup_data(Singup_data)
        error_text=""
        if(Problems[0] is not None):
            error_text=Problems[0]
        elif(Problems[1] is not None):
            error_text=Problems[1]  
        elif(Problems[2] is not None):
            error_text=Problems[2]  
        
        if(len(error_text)>40):
          error_text=Wrap_over_newline(error_text,40)

        if(error_text!=""): 
           Error_label.config(text=error_text)   #if there is an error, display it
        else:
            Signup_Window.destroy()
            Create_User_Account(Singup_data)   

   Submit_button = tkinter.Button(user_input_frame, bg="blue" , text="Sign up",command=Submit_Singup_data, **Button_style_2,**Basic_Button_style)
   Submit_button.grid(row=6,column=0,padx=(0,200),pady=(20,10)) 

   login_instead_button = tkinter.Button(user_input_frame, bg="Green" , text="Login\nInstead",command=lambda: Sign_up_to_login(Signup_Window), **Button_style_2,**Basic_Button_style)
   login_instead_button.grid(row=6,column=0,padx=(200,0),pady=(20,10)) 

    #binding fields to the event when cursor is placed in input fields (basically handles placeholder values being displayed or not)
   name_entry.bind("<FocusIn>", lambda event: on_focus_in(event, name_entry, name_placeholder))
   name_entry.bind("<FocusOut>", lambda event: on_focus_out(event, name_entry, name_placeholder))

   Password_entry.bind("<FocusIn>", lambda event: on_focus_in(event, Password_entry, password_placeholder))
   Password_entry.bind("<FocusOut>", lambda event: on_focus_out(event, Password_entry, password_placeholder))

   Confirm_entry.bind("<FocusIn>", lambda event: on_focus_in(event, Confirm_entry, Confirm_placeholder))
   Confirm_entry.bind("<FocusOut>", lambda event: on_focus_out(event, Confirm_entry, Confirm_placeholder))

   email_entry.bind("<FocusIn>", lambda event: on_focus_in(event, email_entry, email_placeholder))
   email_entry.bind("<FocusOut>", lambda event: on_focus_out(event, email_entry, email_placeholder))

   Signup_Window.mainloop()
# -------------------------------------Sign Up window ENDS ------------------------------------------------------------------


 # --------------------------- Login window ---------------------------------------------------------------------------
def Login_Function():
   
   login_Window = tkinter.Tk()
   login_Window.title("Login Window")  # Title forlogin_Window
   login_Window.geometry(f"465x420+{X_cord}+{Y_cord}")  # Size forlogin_Window
   login_Window.config(bg="black")  # Set background color oflogin_Window
   
   name_placeholder = "Username"
   password_placeholder = "Password"

   Welcomelabel=tkinter.Label(login_Window,font=Other_Headings_font, bg="black", fg="Red" ,text="Login") 
   Welcomelabel.grid(pady=(10,10))
   
   login_frame=tkinter.LabelFrame(login_Window)
   login_frame.grid(row=1,column=0 ,padx=20,pady=10)

   name_entry=tkinter.Entry(login_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   name_entry.grid(row=1,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   name_entry.insert(0, name_placeholder)

   Password_entry=tkinter.Entry(login_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   Password_entry.grid(row=2,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   Password_entry.insert(0, password_placeholder)

   # when the user clicks on the submit button, this field becomes visible and displays errors (if any)
   Error_label=tkinter.Label(login_frame,font=Simple_text_font, fg="Red", justify="left",text="")  
   Error_label.grid(row=3,column=0,pady=(10,10))    

   def submit_login_data():  #nested functiion to get field values and display possible errors
        login_data = [
            name_entry.get(),  
            Password_entry.get(),  
        ]

        if(login_data[0]=="Admin" and login_data[1]=="Fast1234"): #Hardcoded Username and Password for admin.
            login_Window.destroy()
            Show_Admin_Account()
            return None

        Acount_Id=0
        Validation_result = Validate_login_data(login_data)  #index 0 is error, index 1 is id
        error_text=""
        if(Validation_result[0] is not None):
            error_text=Validation_result[0] 
        else:
            Acount_Id=Validation_result[1]
        
        if(error_text!=""):                    #if there is an error, display it
           Error_label.config(text=error_text)
        else:
            login_Window.destroy()
            Show_User_Account(int(Acount_Id))

   Submit_button = tkinter.Button(login_frame, bg="green" , text="Login",command=submit_login_data,**Button_style_2,**Basic_Button_style)
   Submit_button.grid(row=4,column=0,padx=(0,200),pady=(20,10)) 


   Sign_up_instead_button = tkinter.Button(login_frame, bg="blue" , text="Sign up\nInstead",command=lambda:login_to_Sign_up(login_Window),**Button_style_2,**Basic_Button_style)
   Sign_up_instead_button.grid(row=4,column=0,padx=(200,0),pady=(20,10))

   name_entry.bind("<FocusIn>", lambda event: on_focus_in(event, name_entry, name_placeholder))
   name_entry.bind("<FocusOut>", lambda event: on_focus_out(event, name_entry, name_placeholder))

   Password_entry.bind("<FocusIn>", lambda event: on_focus_in(event, Password_entry, password_placeholder))
   Password_entry.bind("<FocusOut>", lambda event: on_focus_out(event, Password_entry, password_placeholder))

   login_Window.mainloop()
# -----------------------------------------------------------------------------------------------------------------------------------

def main():
# Creating the main window
    MainWindow = tkinter.Tk()
    MainWindow.title("Login/Signup Window")  # Set the window title
    MainWindow.geometry(f"465x400+{X_cord}+{Y_cord}")  # Set the window size (width x height)
    MainWindow.config(bg="black")

#main Label
    App_name_label=tkinter.Label(MainWindow,font=Main_Heading_font, bg="black", fg="red" ,text="Transctions 101") 
    App_name_label.pack(pady=(10,45))

    Sign_up_button = tkinter.Button(MainWindow , bg="green", text="Sign up",command=lambda: main_to_Sign_up(MainWindow),**Button_style_1,**Basic_Button_style)
    Sign_up_button.pack(pady=(15,10))

    log_in_button = tkinter.Button(MainWindow, bg="blue" , text="Log in", command=lambda: main_to_login(MainWindow), **Button_style_1,**Basic_Button_style)
    log_in_button.pack(pady=(15,0)) 

    MainWindow.mainloop()
main()