from tkinter import*
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import mysql.connector

class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Patient Registration")
        self.root.geometry('1600x900+0+0')

        #variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_SecurityQ = StringVar()
        self.var_SecurityA = StringVar()
        self.var_passwd = StringVar()
        self.var_passwdcnf = StringVar()


        # background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root , image=self.bg)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\pat.jpg")
        bg1_label = Label(self.root, image=self.bg1)
        bg1_label.place(x=50, y=100, width=470, height=550)

        #main frame
        frame = Frame(self.root , bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        #register here text
        register_lbl = Label(frame , text="Register here" , font=("calibri",25,"bold"),fg="green",bg="white")
        register_lbl.place(x=20,y=20)

        # =====================    label and entry part ===========================


        #first row
        fname = Label(frame , text="First name" , font=("calibri",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry = ttk.Entry(frame, textvariable = self.var_fname,font=("calibri",15))
        self.fname_entry.place(x=50,y=130,width=250)

        lname = Label(frame, text="Last name", font=("calibri", 15, "bold"), bg="white")
        lname.place(x=370, y=100)

        self.lname_entry=ttk.Entry(frame,textvariable = self.var_lname ,font=("calibri",15))
        self.lname_entry.place(x=370,y=130,width=250)



        #second row
        contact = Label(frame, text="Contact No", font=("calibri", 15, "bold"), bg="white")
        contact.place(x=50, y=170)

        self.contact_entry = ttk.Entry(frame,textvariable = self.var_contact, font=("calibri", 15))
        self.contact_entry.place(x=50, y=200, width=250)

        email = Label(frame, text="Enter email ID", font=("calibri", 15, "bold"), bg="white")
        email.place(x=370, y=170)

        self.email_entry = ttk.Entry(frame,textvariable = self.var_email, font=("calibri", 15))
        self.email_entry.place(x=370, y=200, width=250)

        #third row
        SecurityQ = Label(frame, text="Choose Security Question", font=("calibri", 15, "bold"), bg="white")
        SecurityQ.place(x=50, y=240)

        self.SecurityQ_entry = ttk.Combobox(frame,textvariable = self.var_SecurityQ, font=("calibri", 15),state="readonly")
        self.SecurityQ_entry["values"] = ("a","b","c","d")
        self.SecurityQ_entry.place(x=50, y=270, width=250)
        self.SecurityQ_entry.current(0)

        SecurityA = Label(frame, text="Answer", font=("calibri", 15, "bold"), bg="white")
        SecurityA.place(x=370, y=240)

        self.SecurityA_entry = ttk.Entry(frame,textvariable = self.var_SecurityA, font=("calibri", 15))
        self.SecurityA_entry.place(x=370, y=270, width=250)


        #fourth row
        passwd = Label(frame, text="Enter password", font=("calibri", 15, "bold"), bg="white")
        passwd.place(x=50, y=310)

        self.passwd_entry = ttk.Entry(frame,textvariable = self.var_passwd, font=("calibri", 15))
        self.passwd_entry.place(x=50, y=340, width=250)

        passwdcnf = Label(frame, text="Confirm Password", font=("calibri", 15, "bold"), bg="white")
        passwdcnf.place(x=370, y=310)

        self.passwdcnf_entry = ttk.Entry(frame,textvariable = self.var_passwdcnf, font=("calibri", 15))
        self.passwdcnf_entry.place(x=370, y=340, width=250)

        #checkbox
        self.var_chkbox = IntVar()
        chkbox = Checkbutton(frame ,variable = self.var_chkbox, text="I agree terms and conditions" , font=("calibri", 15, "bold") , onvalue=1,offvalue=0)
        chkbox.place(x=50,y=390)

        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\submit.jpg")
        img = img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame ,image=self.photoimage , command = self.registerdata , borderwidth=0 , cursor="hand2")
        b1.place(x=100,y=440,width=200)


        ########### function declaration

    def registerdata(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_SecurityQ.get()=="Select":
            messagebox.showerror("Error" , "Please fill all the fields")
        elif self.var_passwd.get()!=self.var_passwdcnf.get():
            messagebox.showerror("Error","Both passwords must match")
        elif self.var_chkbox.get()==0:
            messagebox.showerror("Error" , "Please agree terms and conditions")
        else :
            conn = mysql.connector.connect(host="localhost",user="root",password="0000",database="hms")
            my_cur = conn.cursor()
            query = ("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cur.execute(query,value)
            row = my_cur.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist/registered")
            else:
                my_cur.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(self.var_fname.get(),self.var_lname.get() ,self.var_contact.get(), self.var_email.get(),self.var_SecurityQ.get() , self.var_SecurityA.get() , self.var_passwd.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success" , "Registered Succesfully")





if __name__ == "__main__" :
    root=Tk()
    app = Register(root)
    root.mainloop()