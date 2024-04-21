from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

def main():
    win = Tk()
    app = Admin_Login_Window(win)
    win.mainloop()

class Admin_Login_Window:
    def __init__(self, root):
        self.root=root
        self.root.title("Admin Login")
        self.root.geometry("1550x800+0+0")

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\login.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame
        frame = Frame(self.root, bg="white")
        frame.place(x=610, y=170, width=340, height=470)

        img1 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\admindp.jpg")
        img1 = img1.resize((100, 100), Image.ANTIALIAS)
        self.photoimage = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimage,bg="white",borderwidth=0)
        lblimg1.place(x=730, y=175, width=100 , height =100)


        get_str = Label(frame,text="Admin Login" , font=("calibri",20,"bold"),fg="black" , bg="white")
        get_str.place(x=95,y=100)

        #label
        username=lbl=Label(frame,text="User Name",font=("calibri",15,"bold"),fg="black" , bg="white")
        username.place(x=70,y=155)
        self.txtuser=Entry(frame ,font=("calibri",15) )
        self.txtuser.place(x=40 , y=180 ,width=270)

        password = lbl = Label(frame, text="Password", font=("calibri", 15, "bold"), fg="black", bg="white")
        password.place(x=70, y=225)
        self.txtpass = Entry(frame, font=("calibri", 15))
        self.txtpass.place(x=40, y=250, width=270)

        #icon images
        img2 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\username.jpg")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(image=self.photoimage2, bg="white", borderwidth=0)
        lblimg2.place(x=650, y=323, width=25, height=25)

        img3 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\pass.jpg")
        img3 = img3.resize((25, 25), Image.ANTIALIAS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        lblimg3 = Label(image=self.photoimage3, bg="white", borderwidth=0)
        lblimg3.place(x=650, y=395, width=25, height=25)

        #login button
        loginbtn = Button(frame ,command = self.login ,text="Login" ,font=("calibri", 15, "bold"),bd=3 , relief = RIDGE , fg="black" , bg="#99ccff",activeforeground="white",activebackground="#99ccff")
        loginbtn.place(x=110,y=300,width=120,height=35)


        #register button
        registerbtn = Button(frame, command = self.register_window , text="New user ?",borderwidth=0, font=("calibri", 8, "bold"), bd=3,  fg="white", bg="#1a8cff",
                          activeforeground="white", activebackground="blue")
        registerbtn.place(x=90, y=350, width=160)


        #forget password button
        forgotbtn = Button(frame,command= self.forgot_password_window, text="Forgot password?",borderwidth=0, font=("calibri", 8, "bold"), bd=3,  fg="white",
                             bg="#1a8cff",
                             activeforeground="white", activebackground="blue")
        forgotbtn.place(x=90, y=380, width=160)


    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)


    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="" :
            messagebox.showerror("Error" , "Please fill all fields!!")

        elif self.txtuser.get()=="abhi" and self.txtpass.get()=="0000":
            messagebox.showinfo("Success" ,"Ho gaya login")

        else :
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            my_cur.execute("select * from register where email=%s and passwd=%s",
                           (self.txtuser.get() , self.txtpass.get()))
            row = my_cur.fetchone()
            if row==None :
                messagebox.showerror("Error" , "Invalid username and password")
            else:
                open_main=messagebox.askyesno("YesNo","Granting Admin access")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Menupage(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()


    def reset_password(self):
        if self.SecurityQ_entry.get()=="a":
            messagebox.showerror("Error","Select the security question" , parent=self.root2)
        elif self.SecurityA_entry.get()=="":
            messagebox.showerror("Error", "Enter the answer", parent=self.root2)
        elif self.newpasswd_entry.get()=="":
            messagebox.showerror("Error", "Please enter a new password", parent=self.root2)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from register where email=%s and SecurityQ=%s and SecurityA=%s"
            value = (self.txtuser.get(),self.SecurityQ_entry.get(),self.SecurityA_entry.get())
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct answer", parent=self.root2)
            else :
                query = "update register set passwd=%s where email=%s"
                value = (self.newpasswd_entry.get() ,self.txtuser.get())
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Your  password has been resetted , login with new credentials" , parent=self.root2)
                self.root2.destroy()


    def forgot_password_window(self) :
        if self.txtuser.get()=="" :
            messagebox.showerror("Error" ,"Please enter email to reset password" )
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from register where email=%s"
            value = (self.txtuser.get(),)
            my_cur.execute(query,value)
            row = my_cur.fetchone()

            if row==None :
                messagebox.showerror("Error","Please enter valid username")
            else :
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Reset Password")
                self.root2.geometry("340x450+610+170")

                l= Label(self.root2,text="Forgot Password", font=("calibri", 20, "bold"), fg="white",  bg="white")
                l.place(x=0,y=10,relwidth=1)

                SecurityQ = Label(self.root2, text="Choose Security Question", font=("calibri", 15, "bold"), bg="white",fg="black")
                SecurityQ.place(x=50, y=80)

                self.SecurityQ_entry = ttk.Combobox(self.root2, font=("calibri", 15),state="readonly")
                self.SecurityQ_entry["values"] = ("a", "b", "c", "d")
                self.SecurityQ_entry.place(x=50, y=110, width=250)
                self.SecurityQ_entry.current(0)

                SecurityA = Label(self.root2, text="Answer", font=("calibri", 15, "bold"), bg="white" ,fg="black")
                SecurityA.place(x=50, y=150)
                self.SecurityA_entry = ttk.Entry(self.root2, font=("calibri", 15))
                self.SecurityA_entry.place(x=50, y=180, width=250)

                newpasswd = Label(self.root2, text="New Password", font=("calibri", 15, "bold"), bg="white", fg="black")
                newpasswd.place(x=50, y=220)
                self.newpasswd_entry = ttk.Entry(self.root2, font=("calibri", 15))
                self.newpasswd_entry.place(x=50, y=250, width=250)

                btn=Button(self.root2,command = self.reset_password, text="Reset",font=("calibri", 15,"bold") , fg="white",bg="blue")
                btn.place(x=100,y=290)

class Menupage:
    def __init__(self,root):
        self.root = root
        self.root.title("Home Menu Page")
        self.root.geometry('1600x900+0+0')

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # f1 for patients
        f1 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f1.place(x=50, y=150, width=300, height=200)
        # buttons part
        img1 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu1.jpg")
        img1 = img1.resize((300, 200), Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        b1 = Button(f1, command= self.patient_window , image=self.photoimage1,  borderwidth=0, cursor="hand2")
        b1.place(x=0, y=0, width=300)
        name1 = Label(self.root, text="Patients ", font=("calibri", 15, "bold"), bg="white")
        name1.place(x=50, y=120)



        #f2 for doctors
        f2 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f2.place(x=430, y=150, width=300, height=200)
        img2 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu2.jpg")
        img2 = img2.resize((300, 200), Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        b2 = Button(f2, image=self.photoimage2, borderwidth=0, cursor="hand2")
        b2.place(x=0, y=0, width=300)
        name2 = Label(self.root, text="Doctors ", font=("calibri", 15, "bold"), bg="white")
        name2.place(x=430, y=120)



        #f3 for appointments
        f3 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f3.place(x=810, y=150, width=300, height=200)
        img3 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu3.jpg")
        img3 = img3.resize((300, 200), Image.ANTIALIAS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        b3 = Button(f3, image=self.photoimage3, borderwidth=0, cursor="hand2")
        b3.place(x=0, y=0, width=300)
        name3 = Label(self.root, text="Appointments", font=("calibri", 15, "bold"), bg="white")
        name3.place(x=810, y=120)


        #f4 for staffs
        f4 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f4.place(x=1190, y=150, width=300, height=200)
        img4 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu4.jpg")
        img4 = img4.resize((300, 200), Image.ANTIALIAS)
        self.photoimage4 = ImageTk.PhotoImage(img4)
        b4 = Button(f4, image=self.photoimage4, borderwidth=0, cursor="hand2")
        b4.place(x=0, y=0, width=300)
        name4 = Label(self.root, text="Staffs ", font=("calibri", 15, "bold"), bg="white")
        name4.place(x=1190, y=120)


        #f5 for beds
        f5 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f5.place(x=50, y=450, width=300, height=200)
        img5 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu5.jpg")
        img5 = img5.resize((300, 200), Image.ANTIALIAS)
        self.photoimage5 = ImageTk.PhotoImage(img5)
        b5 = Button(f5, image=self.photoimage5, borderwidth=0, cursor="hand2")
        b5.place(x=0, y=0, width=300)
        name5 = Label(self.root, text="Staffs ", font=("calibri", 15, "bold"), bg="white")
        name5.place(x=50, y=420)


        #f6 for emergency
        f6 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f6.place(x=430, y=450, width=300, height=200)
        img6 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu6.jpg")
        img6 = img6.resize((300, 200), Image.ANTIALIAS)
        self.photoimage6 = ImageTk.PhotoImage(img6)
        b6 = Button(f6, image=self.photoimage6, borderwidth=0, cursor="hand2")
        b6.place(x=0, y=0, width=300)
        name6 = Label(self.root, text="Emergency ", font=("calibri", 15, "bold"), bg="white")
        name6.place(x=430, y=420)


        #f7 for admin
        f7 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f7.place(x=810, y=450, width=300, height=200)
        img7 = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\menu7.jpg")
        img7 = img7.resize((300, 200), Image.ANTIALIAS)
        self.photoimage7 = ImageTk.PhotoImage(img7)
        b7 = Button(f7, image=self.photoimage7, borderwidth=0, cursor="hand2")
        b7.place(x=0, y=0, width=300)
        name7 = Label(self.root, text="Admin ", font=("calibri", 15, "bold"), bg="white")
        name7.place(x=810, y=420)

    def patient_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Patient(self.new_window)



class Patient:
    def __init__(self,root):
        self.root = root
        self.root.title("Patient Registration")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_gender = StringVar()
        self.var_blood = StringVar()
        self.var_admitdate = StringVar()
        self.var_dischargedate = StringVar()
        self.var_contact = StringVar()
        self.var_status = StringVar()
        self.var_symptoms = StringVar()
        self.var_department = StringVar()
        self.var_address = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4 ,bg="white" , relief = RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450 )

        scroll_x = ttk.Scrollbar(rowframe,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.patienttable=ttk.Treeview(rowframe , column=("PID" , "First name","Last name","Gender" ,"Blood Type" , "Contact No" ,"Address" , "Admit on" , "Discharge on" , "Status" ,"Symptom" ,"Department"),xscrollcommand=scroll_x.set , yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM ,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.patienttable.xview)
        scroll_y.config(command=self.patienttable.yview)

        self.patienttable.heading("PID",text="PID")
        self.patienttable.heading("First name", text="First name")
        self.patienttable.heading("Last name", text="Last name")
        self.patienttable.heading("Gender", text="Gender")
        self.patienttable.heading("Blood Type", text="Blood Type")
        self.patienttable.heading("Contact No", text="Contact No")
        self.patienttable.heading("Address", text="Address")
        self.patienttable.heading("Admit on", text="Admit on")
        self.patienttable.heading("Discharge on", text="Discharge on")
        self.patienttable.heading("Status", text="Status")
        self.patienttable.heading("Symptom", text="Symptom")
        self.patienttable.heading("Department", text="Department")

        self.patienttable["show"]="headings"
        self.patienttable.column("PID",width=100)
        self.patienttable.column("First name", width=100)
        self.patienttable.column("Last name", width=100)
        self.patienttable.column("Gender", width=100)
        self.patienttable.column("Blood Type", width=100)
        self.patienttable.column("Contact No", width=100)
        self.patienttable.column("Address", width=200)
        self.patienttable.column("Admit on", width=100)
        self.patienttable.column("Discharge on", width=100)
        self.patienttable.column("Status", width=100)
        self.patienttable.column("Symptom", width=200)
        self.patienttable.column("Department", width=100)

        self.patienttable.pack(fill=BOTH,expand=1)
        self.fetch_entries()


        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        registerpat = Button(topframe,command=self.patient_register_window, text="Register New Patient", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                               fg="white", bg="blue", activeforeground="white", activebackground="blue")
        registerpat.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe,command = self.update_data, text="Update Patient Details", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, text="Discharge Patient", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
        dischargepat.place(x=480, y=10, width=200, height=50)

        extbtn = Button(topframe, text="Exit", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="blue", activeforeground="white", activebackground="blue")
        extbtn.place(x=1270, y=10, width=100, height=50)


        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Patients:", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=950, y=10)

        self.blood_entry = ttk.Combobox(navframe, font=("calibri", 15), state="readonly")
        self.blood_entry["values"] = ("Select", "A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-")
        self.blood_entry.place(x=1050, y=10, width=100)
        self.blood_entry.current(0)

        self.fromdate_entry = ttk.Entry(navframe, font=("calibri", 15))
        self.fromdate_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                            fg="white", bg="blue", activeforeground="white", activebackground="blue")
        nsearchbtn.place(x=1290, y=5, width=100)


        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        fromdate = Label(botframe, text="From date", font=("calibri", 15, "bold"), bg="white")
        fromdate.place(x=5, y=10)
        self.fromdate_entry = ttk.Entry(botframe,  font=("calibri", 15))
        self.fromdate_entry.place(x=100, y=10, width=100)

        tilldate = Label(botframe, text="Till date", font=("calibri", 15, "bold"), bg="white")
        tilldate.place(x=210, y=10)
        self.fromdate_entry = ttk.Entry(botframe, font=("calibri", 15))
        self.fromdate_entry.place(x=290, y=10, width=100)

        bsearchbtn = Button(botframe,  text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                          fg="white", bg="blue", activeforeground="white", activebackground="blue")
        bsearchbtn.place(x=410, y=5, width=100 ,height=40)

        showallbutton = Button(botframe, text="Show All", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                          fg="white", bg="blue", activeforeground="white", activebackground="blue")
        showallbutton.place(x=1250, y=5, width=120, height=35)


    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from patient")
        data=my_cur.fetchall()
        if len(data)!=0:
            self.patienttable.delete(*self.patienttable.get_children())
            for i in data:
                self.patienttable.insert("",END,values=i)
                conn.commit()
            conn.close()

    def update_data(self):
        if self.var_firstname.get() == "" or self.var_lastname.get() == "" or self.var_address.get() == "" or self.var_symptoms.get() == "" or self.var_admitdate == "" or self.var_gender.get() == "Select" or self.var_blood.get() == "Select" or self.var_status.get() == "Select" or self.var_department.get() == "Select":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                update=messagebox.askyesno("Updating","Do  you surely want to update",parent=self.root)
                if update>0:
                    conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                    my_cur = conn.cursor()
                    my_cur.execute(
                        "update patient set firstname=%s,lastname=%s,gender=%s,blood=%s,contact=%s,address=%s,admitdate=%s,dischargedate=%s,status=%s,symptom=%s,department=%s where pid=%s",
                        (self.var_firstname.get(),
                         self.var_lastname.get(),
                         self.var_gender.get(),
                         self.var_blood.get(),
                         int(self.var_contact.get()),
                         self.var_address.get(),
                         self.var_admitdate.get(),
                         self.var_dischargedate.get(),
                         self.var_status.get(),
                         self.var_symptoms.get(),
                         self.var_department.get(),
                         self.var_pid.get()))
                else:
                    if not update:
                        return

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Updated Succesfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to{str(es)}",parent=self.root)


    def patient_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Patient_Register(self.new_window)



class Patient_Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Patient Registration")
        self.root.geometry('1600x900+0+0')

        #variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_gender = StringVar()
        self.var_blood = StringVar()
        self.var_admitdate = StringVar()
        self.var_dischargedate = StringVar()
        self.var_contact = StringVar()
        self.var_status = StringVar()
        self.var_symptoms = StringVar()
        self.var_department = StringVar()
        self.var_address = StringVar()


        # background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root , image=self.bg)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\pat.jpg")
        bg1_label = Label(self.root, image=self.bg1)
        bg1_label.place(x=50, y=100, width=470, height=600)

        #main frame
        frame = Frame(self.root , bg="white")
        frame.place(x=520,y=100,width=800,height=600)

        #register here text
        register_lbl = Label(frame , text="Register here" , font=("calibri",25,"bold"),fg="green",bg="white")
        register_lbl.place(x=20,y=20)

        # =====================    label and entry part ===========================


        #first row
        firstname = Label(frame , text="First name" , font=("calibri",15,"bold"),bg="white")
        firstname.place(x=50,y=100)

        self.firstname_entry = ttk.Entry(frame, textvariable = self.var_firstname,font=("calibri",15))
        self.firstname_entry.place(x=50,y=130,width=250)

        lastname = Label(frame, text="Last name", font=("calibri", 15, "bold"), bg="white")
        lastname.place(x=370, y=100)

        self.lastname_entry=ttk.Entry(frame,textvariable = self.var_lastname ,font=("calibri",15))
        self.lastname_entry.place(x=370,y=130,width=250)



        #second row
        Gender = Label(frame, text="Gender", font=("calibri", 15, "bold"), bg="white")
        Gender.place(x=50, y=170)
        self.Gender_entry = ttk.Combobox(frame, textvariable=self.var_gender, font=("calibri", 15),state="readonly")
        self.Gender_entry["values"] = ("Select", "Male", "Female", "Other")
        self.Gender_entry.place(x=50, y=200, width=250)
        self.Gender_entry.current(0)


        blood = Label(frame, text="Blood Type", font=("calibri", 15, "bold"), bg="white")
        blood.place(x=370, y=170)
        self.blood_entry = ttk.Entry(frame,textvariable = self.var_blood, font=("calibri", 15))
        self.blood_entry.place(x=370, y=200, width=250)

        self.blood_entry = ttk.Combobox(frame, textvariable=self.var_blood, font=("calibri", 15), state="readonly")
        self.blood_entry["values"] = ("Select", "A+", "B+", "AB+","O+","A-", "B-", "AB-","O-")
        self.blood_entry.place(x=370, y=200, width=250)
        self.blood_entry.current(0)


        #third row

        contact = Label(frame, text="Contact", font=("calibri", 15, "bold"), bg="white")
        contact.place(x=50, y=240)
        self.contact_entry = ttk.Entry(frame, textvariable=self.var_contact, font=("calibri", 15))
        self.contact_entry.place(x=50, y=270, width=250)

        status = Label(frame, text="Status", font=("calibri", 15, "bold"), bg="white")
        status.place(x=370, y=240)
        self.status_entry = ttk.Combobox(frame,textvariable = self.var_status, font=("calibri", 15),state="readonly")
        self.status_entry["values"] = ("Select","Admitted","Discharged")
        self.status_entry.place(x=370, y=270, width=250)
        self.status_entry.current(0)


        #fourth row
        admitdate = Label(frame, text="Admit date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        admitdate.place(x=50, y=310)
        self.admitdate_entry = ttk.Entry(frame,textvariable = self.var_admitdate, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=340, width=250)

        dischargedate = Label(frame, text="Discharge date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        dischargedate.place(x=370, y=310)
        self.dischargedate_entry = ttk.Entry(frame,textvariable = self.var_dischargedate, font=("calibri", 15))
        self.dischargedate_entry.place(x=370, y=340, width=250)


        # fifth row
        address = Label(frame, text="Address ", font=("calibri", 15, "bold"), bg="white")
        address.place(x=50, y=380)
        self.admitdate_entry = ttk.Entry(frame, textvariable=self.var_address, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=410, width=250)

        symptoms = Label(frame, text="Symptoms ", font=("calibri", 15, "bold"), bg="white")
        symptoms.place(x=370, y=380)
        self.symptoms_entry = ttk.Entry(frame, textvariable=self.var_symptoms, font=("calibri", 15))
        self.symptoms_entry.place(x=370, y=410, width=250)


        #row 6

        department = Label(frame, text="Department ", font=("calibri", 15, "bold"), bg="white")
        department.place(x=50, y=450)
        self.department_entry = ttk.Combobox(frame, textvariable=self.var_department, font=("calibri", 15), state="readonly")
        self.department_entry["values"] = ("Select", "General", "Gynaechology","Dental","Cardiology","Neurology","Dermatology","Radiology","Surgical")
        self.department_entry.place(x=50, y=480, width=250)
        self.department_entry.current(0)


        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\submit.jpg")
        img = img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame ,image=self.photoimage , command = self.registerdata , borderwidth=0 , cursor="hand2")
        b1.place(x=370,y=480,width=200)


        ########### function declaration

    def registerdata(self):
        if self.var_firstname.get()=="" or self.var_lastname.get()=="" or self.var_address.get()=="" or self.var_symptoms.get()=="" or self.var_admitdate=="" or self.var_gender.get()=="Select" or self.var_blood.get()=="Select" or self.var_status.get()=="Select" or self.var_department.get()=="Select" :
            messagebox.showerror("Error" , "Please fill all the fields")

        else :
            conn = mysql.connector.connect(host="localhost",user="root",password="0000",database="hms")
            my_cur = conn.cursor()
            my_cur.execute("insert into patient (firstname,lastname,gender,blood,contact,address,admitdate,dischargedate,status,symptom,department) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.var_firstname.get(),
                            self.var_lastname.get() ,
                            self.var_gender.get(),
                            self.var_blood.get(),
                            int(self.var_contact.get()) ,
                            self.var_address.get() ,
                            self.var_admitdate.get(),
                            self.var_dischargedate.get(),
                            self.var_status.get(),
                            self.var_symptoms.get(),
                            self.var_department.get()))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success" , "Registered Succesfully")



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


if __name__ == "__main__":
    main()