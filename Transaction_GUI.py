# pip install Pillow (install if you havent already)

import tkinter
from datetime import datetime
from tkinter import filedialog

from PIL import Image, ImageTk

import qr_code
from Filing_logic import *
from rsa import *
from sha1 import calculate_sha1

X_cord=600  
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


#Incomplete Functions -------------------------------------------------------------------------

def RSA_Encryption_and_message_hash(Username,Amount,Message,Time_of_generation,Reciever_Public_key):
    signature = f"{Username} {Amount} {Message} {Time_of_generation}"
    Username = encrypt(Reciever_Public_key, Username)
    Amount = encrypt(Reciever_Public_key, str(Amount))
    Message = encrypt(Reciever_Public_key, Message)
    HASH_of_MSG=calculate_sha1(signature)
    temporary_testing_list=[Username, Amount, Message, Time_of_generation, HASH_of_MSG]
    return temporary_testing_list

def RSA_decryption_msg(QR_name,QR_amount,QR_msg,Reciever_Private_key):
    QR_data_list=[]

    QR_name = QR_name.strip("[]")
    QR_name = QR_name.split(", ")
    QR_name = [int(num) for num in QR_name]
    
    QR_amount = QR_amount.strip("[]")
    QR_amount = QR_amount.split(", ")
    QR_amount = [int(num) for num in QR_amount]
    
    QR_msg = QR_msg.strip("[]")
    QR_msg = QR_msg.split(", ")
    QR_msg = [int(num) for num in QR_msg]
    
    QR_data_list.append(decrypt(Reciever_Private_key, QR_name))
    QR_data_list.append(decrypt(Reciever_Private_key, QR_amount))
    QR_data_list.append(decrypt(Reciever_Private_key, QR_msg))

    return QR_data_list #this will be the deccrypted data



def Generate_QR_Code(QR_code_Data,qr_file_path):  

    #code to generate the QR code here, it should save the QR code in the same folder, and display in the window below made here
    qrCodes = qr_code.generate_qr_code(QR_code_Data[0],QR_code_Data[1],QR_code_Data[2],QR_code_Data[3],QR_code_Data[4])
    qrCodes.save(qr_file_path)
    img = Image.open(qr_file_path)
    img = img.resize((465, 475))
    Generate_QR_Code_Window = tkinter.Tk()
    Generate_QR_Code_Window.title("Generated QR Code")
    Generate_QR_Code_Window.geometry(f"{img.width}x{img.height}+{X_cord}+{Y_cord}")

    tk_image= ImageTk.PhotoImage(master=Generate_QR_Code_Window, image=img)
    canvas = tkinter.Canvas(Generate_QR_Code_Window, width=img.width, height=img.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.image = tk_image # Keeping a reference to the image to prevent it from being lost in the next loop
    Generate_QR_Code_Window.mainloop()


def get_data_from_QR(my_username,Sender_name,Balance_label,Account_Balance,QR_received=None):  #QR_received is the image from which we exctract data from
   

    QR_data_list=qr_code.read_qr_code(QR_received) 
    QR_name = None
    QR_amount = None
    QR_msg = None
    QR_date = None
    QR_signature = None # Regular expression pattern to extract lists of numbers:  [(extracted num)]
    
    # Iterate over each string in the list
    for item in QR_data_list:
        if "Sender's Name:" in item:
            _, QR_name = item.split(": ") # if item is a list of RSA encrypted integers, add it to this list.
        elif "Amount" in item:
            _, QR_amount = item.split(": ")
        elif "Message" in item:
            _, QR_msg = item.split(": ")
        elif "Date" in item:
            _, QR_date = item.split (": ")
        elif "Signature" in item:
            _, QR_signature = item.split(": ")

            
    all_users=get_All_Usernames()
    if ((Sender_name not in all_users) or my_username==Sender_name):
        print("Invalid Sender")
    else:    
        Sender_public_key=get_Public_key(Sender_name)
    Reciever_Private_key=get_Private_key(my_username)

    Transction_information=RSA_decryption_msg(QR_name,QR_amount,QR_msg,Reciever_Private_key) 

    Sender_username=Transction_information[0]

    money_to_recieve=int(Transction_information[1])
    new_balance=Update_Account_Balance(my_username,money_to_recieve)
    balance_text="(Account Balance: " + str(new_balance) + " Rs)"
    Balance_label.config(text=balance_text)

    Message_to_display=Transction_information[2]

    message_verification_with_hash(QR_signature,Sender_public_key,msg)
   

#Incomplete Functions END-------------------------------------------------------------------------


def Complete_Transaction(Entered_data,Current_User,Balance_label,Account_Balance):
    Username=Entered_data[0]
    Amount=Entered_data[1]
    money_to_send=int(Entered_data[1])
    money_to_send*=-1


    new_balance=Update_Account_Balance(Current_User,money_to_send)
    balance_text="(Account Balance: " + str(new_balance) + " Rs)"
    Balance_label.config(text=balance_text) 

    Message="Message: "
    Time_of_generation=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("At Time:", Time_of_generation)
    if(Entered_data[2]==""):
        Message=Message + "No Additional Message"
    else:    
       Message=Message + Entered_data[2]
    Reciever_Public_key=get_Public_key(Entered_data[0])

    qr_file_path=get_QR_File_path(Current_User)
    QR_code_Data=RSA_Encryption_and_message_hash(Username,Amount,Message,Time_of_generation,Reciever_Public_key)
    Generate_QR_Code(QR_code_Data,qr_file_path)



#Validate Send money data Starts -------------------------------------------------------------------------

def Validate_Send_money_data(Entered_data,Current_balance,this_username):
        
        entered_username, entered_amount, custom_msg= Entered_data
        All_Usernames = get_All_Usernames() #extract all usernames that currently exist in file

        def Validade_Username():
            Validation_error=None
            if(entered_username==""):
                Validation_error="Please Enter the Reciever's Username." 
            elif(entered_username==this_username):
                Validation_error="Sender and Reciever can't be the same." 
            elif(entered_username not in All_Usernames):
                Validation_error="User not found." 
            return Validation_error    
    
        def Validade_entered_amount(entered_amount):
     
            Validation_error=None

            if('-' in entered_amount):   
                Validation_error="Entered Amount can not be negative."

            try:   
             entered_amount= int(entered_amount)
            except ValueError:
             return "Invalid Amount. Please enter a valid amount to transfer."
    
            if(entered_amount>int(Current_balance)):
                Validation_error="Entered Amount is more than Current Balance." 

            return  Validation_error 

        UsernameError=Validade_Username()
        amount_error=Validade_entered_amount(entered_amount)
    
        if(UsernameError is not None):
            return UsernameError
        elif(amount_error is not None):
            return amount_error
        elif(len(custom_msg)>150):
            return "Message Can not Exceed 200 Characters"
        else:
            return ""


        

#Validate Send money data ENDS -------------------------------------------------------------------------

#Send Money Function Starts --------------------------------------------------------------------------------------------------------

def go_back(this_window):
    this_window.destroy()

def Send_Money(Current_balance,this_username,Balance_label,Account_Balance):

    Send_Money_window = tkinter.Tk()
    Send_Money_window.title("Send Money") 
    Send_Money_window.geometry(f"570x610+{X_cord}+{Y_cord}") 
    Send_Money_window.config(bg="black")

    ID_label=tkinter.Label(Send_Money_window,font=Sub_Headings_font, bg="black", fg="white" ,text="Enter Transaction Data") 
    ID_label.grid(row=0,column=0,pady=(20,30))

    Send_Money_frame=tkinter.LabelFrame(Send_Money_window) 
    Send_Money_frame.grid(row=1,column=0 ,padx=20,pady=10)

    Button_Frame=tkinter.LabelFrame(Send_Money_window,bg="black",  relief="flat") 
    Button_Frame.grid(row=5,column=0 ,padx=20,pady=10)

    Username_name_label=tkinter.Label(Send_Money_frame,font=Other_labels_font,text="Reciever Username")   #(this is one of the contained labels)
    Username_name_label.grid(row=1,column=0, pady=10, ipady=5)

    Username_name_entry=tkinter.Entry(Send_Money_frame,font=Entry_label_font, bg="white",fg="gray", width=25)
    Username_name_entry.grid(row=1,column=1, padx=10, pady=10, ipady=5,ipadx=5)

    Amount_label=tkinter.Label(Send_Money_frame,font=Other_labels_font,text="Amount to Send (Rs)")
    Amount_label.grid(row=2,column=0, pady=10, ipady=5)

    Amount_entry=tkinter.Entry(Send_Money_frame,font=Entry_label_font, bg="white",fg="gray", width=25)
    Amount_entry.grid(row=2,column=1, padx=10, pady=10, ipady=5)

    Amount_label=tkinter.Label(Send_Money_frame,font=Other_labels_font,text="Custom Message\n(Optional)")
    Amount_label.grid(row=3,column=0, pady=10, ipady=5)

    Custom_msg_entry = tkinter.Text(Send_Money_frame, font=Entry_label_font, bg="white", fg="gray", width=25, height=7, wrap="word")
    Custom_msg_entry.grid(row=3, column=1, padx=5, pady=5)

    Error_label=tkinter.Label(Send_Money_frame,font=Simple_text_font, fg="Red",justify="left",text="")  
    Error_label.grid(row=4,column=0, columnspan=2,pady=(10,20))  

    back_button = tkinter.Button(Button_Frame, bg="#901111", text="Cancel",command=lambda: go_back(Send_Money_window),**Button_style_2,**Basic_Button_style)
    back_button.grid(row=5,column=0, padx=20, pady=(20,10)) 

    def Submit_Send_money_data():
        Entered_data = [
            Username_name_entry.get(),  
            Amount_entry.get(), 
            Custom_msg_entry.get("1.0", "end-1c"), # 1.0 is starting position, end-1c is last line
        ]

        error_text=Validate_Send_money_data(Entered_data,Current_balance,this_username)
        if(error_text!=""):
           Error_label.config(text=error_text)   #if there is an error, display it
        else:
            Send_Money_window.destroy()
            print("Transction Successful")
            Complete_Transaction(Entered_data,this_username,Balance_label,Account_Balance)  

    Submit_Data_button = tkinter.Button(Button_Frame, bg="#13780a" , text="Submit\nData",command=Submit_Send_money_data, **Button_style_2,**Basic_Button_style)
    Submit_Data_button.grid(row=5,column=1,padx=20,pady=(20,10)) 

#Send Money Function Ends --------------------------------------------------------------------------------------------------------  

#Recieve Money Function Starts --------------------------------------------------------------------------------------------------------  
def Recieve_Money(my_Username,Balance_label,Account_Balance):
    Upload_QR_Code =tkinter.Tk()
    Upload_QR_Code.title("QR code selector")
    Upload_QR_Code.config(bg="black")
    Upload_QR_Code.geometry(f"465x600+{X_cord}+{Y_cord}")
    Upload_QR_Code.withdraw()


    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    label =tkinter.Label(Upload_QR_Code)
    label.pack(pady=20,padx=(10,10))

    img = Image.open(file_path)
    img = img.resize((300, 300)) #resizing to display nicely
    QR_received_tk = ImageTk.PhotoImage(master=Upload_QR_Code, image=img)
    label.config(image=QR_received_tk)
    label.image = QR_received_tk


    Sender_name_label = tkinter.Label(Upload_QR_Code,font=Other_labels_font,bg="black",fg="white",text="Enter Sender's Username:-")
    Sender_name_label.pack(pady=(20,10),padx=(10,10))

    Sender_name_entry = tkinter.Entry(Upload_QR_Code, font=Entry_label_font, bg="white",fg="gray", width=25)
    Sender_name_entry.pack(pady=(0,10),padx=(10,10))

    def Submit_data_clicked():
        Sender_name =Sender_name_entry.get()
        get_data_from_QR(my_Username,Sender_name,Balance_label,Account_Balance,file_path)
        Upload_QR_Code.withdraw()


    Submit_Data_button = tkinter.Button(Upload_QR_Code, bg="#13780a" , text="Confirm\nChoice",command=Submit_data_clicked, **Button_style_2,**Basic_Button_style)
    Submit_Data_button.pack(pady=(20,10),padx=(10,10)) 
    Upload_QR_Code.deiconify()

    Upload_QR_Code.mainloop()
#Recieve Money Function Ends --------------------------------------------------------------------------------------------------------  