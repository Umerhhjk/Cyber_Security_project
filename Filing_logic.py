# Making sure the file is always created in the same folder witht he program
import os
current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, 'User_data.txt')

#Incomplete_functions------------------------------------------------------------------------
def hash_Password(Plain_Text):
  return Plain_Text
  
def Generate_Private_key():
  return "TO BE GENERATED"

def Generate_Public_key():
  return "TO BE GENERATED"

#--------------------------------------------------------------------------------------------


#-------------------------- Create Account Procedure Start ------------------------------------
def Save_Account_Info_in_file(toWrite):
  with open(file_path, 'a') as userfile:
    for line in toWrite:
      userfile.write(line)
    print('Account Successfully Created')


def Create_Account(Account_data):
  Username = Account_data[0]
  Email    = Account_data[1]
  Password = hash_Password(Account_data[2])
  Account_balance = 0
  Account_id=int(get_Last_ID())+1
  Private_key=Generate_Private_key()
  Public_key=Generate_Public_key()


  Acount_Information = [
      f'____________________________ Account ID: {Account_id} ____________________________\n',
      f'Username: {Username}\n', f'Email: {Email}\n',
      f'Account Balance: {Account_balance} Rs\n', f'Password: {Password}\n',
      f'Public Key: {Public_key}\n',f'Private Key: {Private_key}\n','\n\n'
  ]
  Save_Account_Info_in_file(Acount_Information)
  return Account_id


def get_Last_ID():
  last_id = 0
  try:
    with open(file_path, 'r') as userFile:
      for line in userFile:
        if "Account ID:" in line:
          try:
            last_id = line.split("Account ID: ")[1].strip().split()[0]
          except ValueError:
            continue
    return last_id
  except FileNotFoundError:
    return 0
#-------------------------- Create Account Procedure END ------------------------------------


#-------------------------- Login Procedure Start -------------------------------------------
def Check_In_File(Input_data):
  Entered_Username = Input_data[0]
  Entered_Password = Input_data[1]
  This_Account_Id="0"

  Username_to_check = f'Username: {Entered_Username}\n'
  Password_to_check = f'Password: {Entered_Password}\n'

  with open(file_path, 'r') as userFile:
    for line in userFile:
      
      if "Account ID:" in line:
            This_Account_Id = line.split("Account ID: ")[1].strip().split()[0] #get this account ID to return if match found
            line= userFile.readline()   #Line now contains username

      if(Username_to_check == line):
          userFile.readline()                 #skip email
          userFile.readline()                 #skip Account Balance
          this_password = userFile.readline()     #get password of this user

          if(Password_to_check == this_password):
            print('Login Successful')
            return This_Account_Id
    
    return "0"
#-------------------------- Login Procedure ENDS -------------------------------------------



#-------------------------- Get Account Details Procedure STARTS ---------------------------


def get_Details(Acount_Id):
    Account_Details=["","",0,"","","",""]

    with open(file_path, 'r') as userFile:
      for line in userFile:
        if("Account ID:" in line and Acount_Id in line):
           line=userFile.readline()
           Account_Details[0]=line.replace("Username: ", "").strip() #Extract Username

           line=userFile.readline()
           Account_Details[1]=line.replace("Email: ", "").strip() #Extract Email

           line=userFile.readline()
           two_parts = line.split("Account Balance: ") #split into 2 parts "Account Balance: " and what follows
           balance_string = two_parts[1].split()[0]       #further split second part into 2, and save first one as balance
           Account_Details[2]= int(balance_string) #Extract Account Balance

           line=userFile.readline()
           Account_Details[3]=line.replace("Password: ", "").strip() #Extract Password

           line=userFile.readline()
           Account_Details[4]=line.replace("Public Key: ", "").strip() #Extract Public Key

           line=userFile.readline()
           Account_Details[5]=line.replace("Private Key: ", "").strip() #Extract Private Key

    Account_Details[6]=Acount_Id
    return Account_Details

#-------------------------- Get Account Details Procedure ENDS ---------------------------