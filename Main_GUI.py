#pip install email-validator
#install this if you havent already
from email_validator import validate_email, EmailNotValidError
import tkinter

from Filing_logic import *

#Font styles --------------------------------------------------
Main_Heading_font= ("Chiller", 45, "bold")
Other_Headings_font= ("Arial Black", 30, "bold")
Simple_text_font= ("Arial", 15, "bold")
Button_font1=("Arial Black", 20, "bold")
Button_font2=("Arial Black", 15, "bold")
Entry_label_font=("Arial", 15)
Other_labels_font=("Arial", 18, "bold")

#incomplete Functions --------------------------------------------------------------------------------------------------

def Show_User_Account(Acount_Id):
    # Creating the main window
    User_Account_Window = tkinter.Tk()
    User_Account_Window.title("Login/Signup Window")  # Set the window title
    User_Account_Window.geometry("550x430")  # Set the window size (width x height)
    User_Account_Window.config(bg="black")

    Account_Details=get_Details(str(Acount_Id)) # found in filing_logic.cpp

    Username,Email,Account_Balance,Password,Public_Key,Private_Key,Acount_Id=Account_Details
    print(Account_Details)

    Welcome_text="Welcome " + Username

#User_Account Label
    ID_label=tkinter.Label(User_Account_Window,font=Main_Heading_font, bg="black", fg="red" ,text=Welcome_text) 
    ID_label.pack(pady=(10,30))

#incomplete Functions END------------------------------------------------------------------------------------------------


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
# ---------------------------------------------------------------------------------------------------   

#Signup data Validation ------------------------------------------------------------------------------------------
def Validate_Signup_data(Singup_data):
    entered_username, entered_email, entered_password, entered_confirm_password = Singup_data

    file_usernames= "" #CORRECT THIS LATER

    def Validade_Username():
        Validation_error=None
        if(entered_username=="Username"):
            Validation_error="Please Enter a Username." 
        elif(len(entered_username)<8):
            Validation_error="Username should be atleast 8 characters long." 
        elif(entered_username in file_usernames):
                Validation_error="Username Already Exists."
        elif any(character in entered_username for character in ['#', '"', '\'','\n','!',':']):
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

#----------------------------------- Signup data Validation ENDS -------------------------------------------------------


#----------------------------------- Login data Validation -------------------------------------------------------------
def Validate_login_data(login_data):
    Account_Id=Check_In_File(login_data)      #function found in filing_logic.py it returns an id if account is found in file, otherwise returns "0"

    Result=[None,0]   #if account is found, we need the id, else we need to print an error, index 0 is error, index 1 is id
    if(Account_Id=="0"):
       Result[0]="Username or Password Is incorrect."
    else:   
        Result[1]=int(Account_Id)
     
    return Result

#----------------------------------- Login data Validation ENDS --------------------------------------------------------





# --------------------------- Sign Up window ---------------------------------------------------------------------------

def Create_User_Account(Singup_data):
    ID=Create_Account(Singup_data)
    Show_User_Account(ID)

def Sign_Up_Function():
   
   Signup_Window = tkinter.Tk()
   Signup_Window.title("Signup Window")  # Title forSignup_Window
   Signup_Window.geometry("470x550")  # Size forSignup_Window
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
   Error_label=tkinter.Label(user_input_frame,font=Simple_text_font, fg="Red" ,text="")  
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
        if(Problems[0]!=None):
            error_text=Problems[0]
        elif(Problems[1]!=None):
            error_text=Problems[1]  
        elif(Problems[2]!=None):
            error_text=Problems[2]  
        
        if(len(error_text)>40):
          error_text=Wrap_over_newline(error_text,40)

        if(error_text!=""): 
           Error_label.config(text=error_text)   #if there is an error, display it
        else:
            Signup_Window.destroy()
            Create_User_Account(Singup_data)   

   Submit_button = tkinter.Button(user_input_frame,font=Button_font2 ,fg="white", bg="blue" , text="Sign up",command=Submit_Singup_data, width=13, height=2)
   Submit_button.grid(row=6,column=0,padx=(0,200),pady=(20,10)) 

   login_instead_button = tkinter.Button(user_input_frame,font=Button_font2 ,fg="white", bg="Green" , text="Login Instead",command=lambda: Sign_up_to_login(Signup_Window), width=13, height=2)
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
   login_Window.geometry("470x450")  # Size forlogin_Window
   login_Window.config(bg="black")  # Set background color oflogin_Window
   
   name_placeholder = "Username"
   password_placeholder = "Password"

   Welcomelabel=tkinter.Label(login_Window,font=Other_Headings_font, bg="black", fg="Red" ,text="Login") 
   Welcomelabel.grid(pady=(10,10))
   
   user_input_frame=tkinter.LabelFrame(login_Window)
   user_input_frame.grid(row=1,column=0 ,padx=20,pady=10)

   name_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   name_entry.grid(row=1,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   name_entry.insert(0, name_placeholder)

   Password_entry=tkinter.Entry(user_input_frame,font=Entry_label_font, bg="white",fg="gray", width=35)
   Password_entry.grid(row=2,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   Password_entry.insert(0, password_placeholder)

   # when the user clicks on the submit button, this field becomes visible and displays errors (if any)
   Error_label=tkinter.Label(user_input_frame,font=Simple_text_font, fg="Red" ,text="")  
   Error_label.grid(row=3,column=0,pady=(10,10))    

   def submit_login_data():  #nested functiion to get field values and display possible errors
        login_data = [
            name_entry.get(),  
            Password_entry.get(),  
        ]

        Acount_Id=0
        Validation_result = Validate_login_data(login_data)  #index 0 is error, index 1 is id
        error_text=""
        if(Validation_result[0]!=None):
            error_text=Validation_result[0] 
        else:
            Acount_Id=Validation_result[1]
        
        if(len(error_text)>40):
          error_text=Wrap_over_newline(error_text,40)

        if(error_text!=""):                    #if there is an error, display it
           Error_label.config(text=error_text)
        else:
            login_Window.destroy()
            Show_User_Account(int(Acount_Id))

   Submit_button = tkinter.Button(user_input_frame,font=Button_font2 ,fg="white", bg="green" , text="Login", width=13, height=2,command=submit_login_data)
   Submit_button.grid(row=4,column=0,padx=(0,200),pady=(60,10)) 


   Sign_up_instead_button = tkinter.Button(user_input_frame,font=Button_font2 ,fg="white", bg="blue" , text="Sign up Instead",command=lambda:login_to_Sign_up(login_Window), width=13, height=2)
   Sign_up_instead_button.grid(row=4,column=0,padx=(200,0),pady=(60,10))

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
    MainWindow.geometry("550x430")  # Set the window size (width x height)
    MainWindow.config(bg="black")

#main Label
    App_name_label=tkinter.Label(MainWindow,font=Main_Heading_font, bg="black", fg="red" ,text="Application Name") 
    App_name_label.pack(pady=(10,30))

#Sign_up Label and button
    Sign_up_Message_label=tkinter.Label(MainWindow, font=Other_labels_font, bg="black",fg="white", text="New here? Sign up Today!") 
    Sign_up_Message_label.pack(pady=(20,0))

    Sign_up_button = tkinter.Button(MainWindow ,font=Button_font1 ,fg="white", bg="green", text="Sign up", width=15, height=1, command=lambda: main_to_Sign_up(MainWindow))
    Sign_up_button.pack(pady=(15,20))

#log in Label and button
    log_in_Message_label=tkinter.Label(MainWindow, font=Other_labels_font, bg="black",fg="white", text="Already have an Account? Login!") 
    log_in_Message_label.pack(pady=(20,0))

    log_in_button = tkinter.Button(MainWindow,font=Button_font1 ,fg="white", bg="blue" , text="Log in", width=15, height=1, command=lambda: main_to_login(MainWindow))
    log_in_button.pack(pady=(15,0)) 

    MainWindow.mainloop()

main()