import os
import re

from des import des_encrypt_message,des_decrypt_message
from rsa import *
from sha1 import *
from datetime import datetime

current_directory = os.path.dirname(__file__)  # Making sure the file is always created in the same folder with the program
file_path = os.path.join(current_directory, 'User_data.txt')
key_file_path= os.path.join(current_directory, 'key.txt')
Qr_file_path=os.path.join(current_directory, 'Closed_QR_codes.txt')

def list_to_strings(Plain_Text):
  string_text=""
  for line in Plain_Text:
   string_text= string_text + line
  return string_text

def set_des_key():
   with open(key_file_path, 'r') as file:
    key_des = file.read()
    return  key_des
   

#-------------------------- Helper Functions Start ------------------------------------------

def Give_name_to_folder(): # gets current time and names the folder.
   
   Current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   Qr_name='\\'  #starting with a \ to seperate name from filepath 
   Qr_name+=Current_time.replace(' ', '_').replace(':', '_').replace('-', '_')   # replacing () ' ', '-' and ':' ) because they caused problems in file paths
   Qr_name+='.png' #adding the png extention, otherwise the qrcode.save assumes the name is part of the folder path
   return Qr_name

def hash_Password(Plain_Text):
  hashed_password=calculate_sha1(Plain_Text)
  return hashed_password

def get_file_data_string():
  try:
    with open(file_path, 'r') as userFile:
     string_data=userFile.read()
     string_data=string_data.split('\n')  #making an iteratable list wrt \n's

     i=0
     while (i < len(string_data)):
        string_data[i]=string_data[i] +'\n' #restoring the \n
        i=i+1

     return  string_data
  except FileNotFoundError:  
     return "File is Empty"

def get_txt_file_data():
  
  File_data=get_file_data_string()
  Data_to_display=""
  for line in File_data:
    Data_to_display= Data_to_display + line
  return Data_to_display


def get_All_Usernames(): #for signing up, Username must be unique, it cant already exist in file
  
  All_Usernames=[]
  File_data=get_file_data_string()

  for line in File_data:
     if("Username: " in line):
        Username=line.replace("Username: ", "").strip() #Extract Username
        All_Usernames.append(Username)
      
  return All_Usernames


def extract_proper_key(keystring):                     # function to slice string from (a,b) format to a and b. returns a list of integers
    match = re.match(r'\((\d+),\s*(\d+)\)', keystring)
    if match:
        part1 = int(match.group(1))
        part2 = int(match.group(2))
        key_pair=[part1,part2]
        return key_pair
    else:
        raise ValueError("String format is incorrect")

#-------------------------- Helper Functions END ---------------------------------------------

#-------------------------- Create Account Procedure Start ------------------------------------
def Save_Account_Info_in_file(toWrite):
  string_data=list_to_strings(toWrite)
  
  with open(file_path, 'a') as userfile:
    userfile.write(string_data)
    print('Account Successfully Created')

def Create_Account(Account_data):
  Username = Account_data[0]
  Email    = Account_data[1]
  Password = hash_Password(Account_data[2])
  Account_balance = 5000     #To oepn an account, you must have atleast 5000 rupees, assuming this money has been deposited in the account
  Account_id=int(get_Last_ID())+1
  
  full_directory_path = os.path.join(current_directory, "CY_Project_USERS")
  user_dir = os.path.join(full_directory_path, Username)
  os.makedirs(user_dir)
  key_des=set_des_key()
  Public_key, Private_key=generate_keypair()
  Public_key = des_encrypt_message(str( Public_key), key_des)
  Private_key = des_encrypt_message(str(Private_key), key_des)

  Acount_Information = [
      f'____________________________ Account ID: {Account_id} ____________________________\n',
      f'Username: {Username}\n', 
      f'Email: {Email}\n',
      f'Account Balance: {Account_balance} Rs\n',
      f'Password: {Password}\n',
      f'Public Key: {Public_key}\n',
      f'Private Key: {Private_key}\n',
      f'Path To User Folder: {user_dir}\n',
      '\n\n'
  ]
  Save_Account_Info_in_file(Acount_Information)
  return Account_id


def get_Last_ID():
  
  File_data=get_file_data_string()
  if(os.path.getsize(file_path) == 0):
     return 0
  
  last_id = 0
  for line in File_data:
        if "Account ID:" in line:
          try:
            last_id = line.split("Account ID: ")[1].strip().split()[0]
          except ValueError:
            continue
  return last_id
  
#-------------------------- Create Account Procedure END ------------------------------------


#-------------------------- Login Procedure Start ------------------------------------------- 
def Check_In_File(Input_data):
  Entered_Username = Input_data[0]
  Entered_Password = Input_data[1]
  Entered_Password=hash_Password(Entered_Password)
  This_Account_Id="0"


  Username_to_check = f'Username: {Entered_Username}\n'
  Password_to_check = f'Password: {Entered_Password}\n'

  File_data=get_file_data_string()
  i = 0
  while (i < len(File_data)):
        
        line = File_data[i]
      
        if "Account ID:" in line:
            This_Account_Id = line.split("Account ID: ")[1].strip().split()[0] #get this account ID to return if match found
            line= File_data[i+1]   #Line now contains username

        if(Username_to_check == line):

          this_password = File_data[i+4]   # skip email and Account Balance and get password of this user
          if(Password_to_check == this_password):
            print('Login Successful')
            return This_Account_Id
        i=i+1  

  return "0"
#-------------------------- Login Procedure ENDS -------------------------------------------



#-------------------------- Get Account Details Procedure STARTS ---------------------------
def get_Details(Acount_Id):
    Account_Details=["","","","","","",""]

    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Account ID:" in line and Acount_Id in line):
           line=File_data[i+1]
           Account_Details[0]=line.replace("Username: ", "").strip() #Extract Username

           line=File_data[i+2]
           Account_Details[1]=line.replace("Email: ", "").strip() #Extract Email

           line=File_data[i+3]
           two_parts = line.split("Account Balance: ") #split into 2 parts "Account Balance: " and what follows
           Account_Details[2] = two_parts[1].split()[0]       #further split second part into 2, and save first one as balance

           line=File_data[i+4]
           Account_Details[3]=line.replace("Password: ", "").strip() #Extract Password

           line=File_data[i+5]
           Account_Details[4]=line.replace("Public Key: ", "").strip() #Extract Public Key (hashed)

           line=File_data[i+6]
           Account_Details[5]=line.replace("Private Key: ", "").strip() #Extract Private Key (hashed)

           break
        i=i+1

    Account_Details[6]=Acount_Id
    return Account_Details

#-------------------------- Get Account Details Procedure ENDS ---------------------------


#-------------------------- Extract Keys and QR file path Procedures Start ---------------------------

def get_Private_key(Username):
    
    Private_key=""
    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+5]
           Private_key=line.replace("Private Key: ", "").strip() #Extract Private Key (hashed)
           key_des=set_des_key()
           Private_key=des_decrypt_message(Private_key,key_des)
           Private_key=extract_proper_key(Private_key)
           return Private_key
        i=i+1
    return ""    

def get_Public_key(Username):
    
    Public_key=""
    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+4]
           Public_key=line.replace("Public Key: ", "").strip() #Extract Public Key (hashed)
           key_des=set_des_key()
           Public_key=des_decrypt_message(Public_key,key_des)
           Public_key=extract_proper_key(Public_key)
           return Public_key
        i=i+1
    return ""   

def get_QR_File_path(Username):
    qr_path=""
    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+6]
           qr_path=line.replace("Path To User Folder: ", "").strip() #Extract Qr code file pathway
           qr_path+=Give_name_to_folder()  #----------------- DEBUGGER's NOtE: remove if doesnt work
           return qr_path
        i=i+1
    return ""   

#-------------------------- Extract  Keys Procedures Ends ---------------------------

def Update_Account_Balance(Username,balance_offset):
     File_data=get_file_data_string()
     i = 0
     while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
            line=File_data[i+2]
            two_parts = line.split("Account Balance: ") #split into 2 parts "Account Balance: " and what follows
            current_balance=two_parts[1].split()[0]       #further split second part into 2, and save first one as balance
            
            try: 
               new_balance=int(current_balance) +balance_offset
               new_Balance_string= f'Account Balance: {new_balance} Rs\n'
               Update_Account_Data(i+2,new_Balance_string,File_data)
               return new_balance
            except ValueError:   
               print("Filing Error: failed to update Balance")

        i=i+1

def Update_Password(Username,new_password):
     new_password=hash_Password(new_password)
     File_data=get_file_data_string()
     i = 0
     while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
            
            try: 
               new_Password_string= f'Password: {new_password}\n'
               Update_Account_Data(i+3,new_Password_string,File_data)
            except ValueError:   
               print("Filing Error: failed to update Password")

        i=i+1


def Update_Account_Data(line_number,new_data,file_data):
       
      file_data[line_number]=new_data
      try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("Erroring deleting file in updation")
        
        with open(file_path, 'w') as file:
            for line in file_data:
              file.write(line)
            print("Account Data updated Successfully")  
    
      except Exception as e:
        print(f"An error occurred: {e}")

def check_old_password(Username,entered_password):
     File_data=get_file_data_string()
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):
            line=File_data[i+3]
            old_password=line.replace("Password: ", "").strip()
            entered_password=hash_Password(entered_password)
            if(entered_password==old_password):
                return 1
            else:
                return 0
        i=i+1  
     print("Error Fetching the password")
     return -1


#-----------------------------------------------------------

def is_QR_code_closed(signature):
   
   with open(Qr_file_path, 'r') as file:
    for line in file:
       line=line.strip()
       if(line==signature):
          return True
    return False   

def close_QR_Code(signature):
   if(is_QR_code_closed(signature)):
      return 1
   else:
      with open(Qr_file_path, 'a') as file:
         signature+='\n'
         file.write(signature)
         return 1
      return 0