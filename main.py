from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

def main():
    win = Tk()
    app = Admin_Login_Window(win)
    win.mainloop()

###################################LOGIN DISPLAY######################################################
class Admin_Login_Window:
    def __init__(self, root):
        self.root=root
        self.root.title("Admin Login")
        self.root.geometry("1550x800+0+0")

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\login.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame
        frame = Frame(self.root, bg="white")
        frame.place(x=610, y=170, width=340, height=470)

        img1 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\admindp.jpg")
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
        img2 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\username.jpg")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(image=self.photoimage2, bg="white", borderwidth=0)
        lblimg2.place(x=650, y=323, width=25, height=25)

        img3 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\pass.jpg")
        img3 = img3.resize((25, 25), Image.ANTIALIAS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        lblimg3 = Label(image=self.photoimage3, bg="white", borderwidth=0)
        lblimg3.place(x=650, y=395, width=25, height=25)

        #login button
        loginbtn = Button(frame ,command = self.login ,text="Login" ,font=("calibri", 15, "bold"),bd=3 , relief = RIDGE , fg="black" , bg="#99ccff",activeforeground="white",activebackground="#99ccff")
        loginbtn.place(x=110,y=300,width=120,height=35)


        #register button
        registerbtn = Button(frame, command = self.register_window , text="New user ?",borderwidth=0, font=("calibri", 8, "bold"), bd=3,  fg="white", bg="#1a8cff",
                          activeforeground="white", activebackground="#1a75ff")
        registerbtn.place(x=90, y=350, width=160)


        #forget password button
        forgotbtn = Button(frame,command= self.forgot_password_window, text="Forgot password?",borderwidth=0, font=("calibri", 8, "bold"), bd=3,  fg="white",
                             bg="#1a8cff",
                             activeforeground="white", activebackground="#1a75ff")
        forgotbtn.place(x=90, y=380, width=160)

        cpbutton = Button(frame, text="Made by     Abhishek Bagde (21535001) ", borderwidth=0,
                           font=("calibri", 9, "bold"), bd=3, fg="black",
                           bg="#75a3a3",
                           activeforeground="white", activebackground="#75a3a3")
        cpbutton.place(x=0, y=445, width=360)

    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)


    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="" :
            messagebox.showerror("Error" , "Please fill all fields!!")

        else :
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            my_cur.execute("select * from admin where email=%s and passwd=%s",
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
        if self.SecurityQ_entry.get()=="Select":
            messagebox.showerror("Error","Select the security question" , parent=self.root2)
        elif self.SecurityA_entry.get()=="":
            messagebox.showerror("Error", "Enter the answer", parent=self.root2)
        elif self.newpasswd_entry.get()=="":
            messagebox.showerror("Error", "Please enter a new password", parent=self.root2)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from admin where email=%s and SecurityQ=%s and SecurityA=%s"
            value = (self.txtuser.get(),self.SecurityQ_entry.get(),self.SecurityA_entry.get())
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct answer", parent=self.root2)
            else :
                query = "update admin set passwd=%s where email=%s"
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
            query = "select * from admin where email=%s"
            value = (self.txtuser.get(),)
            my_cur.execute(query,value)
            row = my_cur.fetchone()

            if row==None :
                messagebox.showerror("Error","Please enter valid username")
            else :
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Reset Password")
                self.root2.geometry("340x450+610+170")

                l = Label(self.root2, text="Forgot Password", font=("calibri", 20, "bold"), fg="white", bg="white")
                l.place(x=0, y=10, relwidth=1)

                SecurityQ = Label(self.root2, text="Choose Security Question", font=("calibri", 15, "bold"), bg="white",
                                  fg="black")
                SecurityQ.place(x=50, y=80)

                self.SecurityQ_entry = ttk.Combobox(self.root2, font=("calibri", 15), state="readonly")
                self.SecurityQ_entry["values"] = ("Select", "Enter birth place", "Enter petname", "Enter bestfriend name")
                self.SecurityQ_entry.place(x=50, y=110, width=250)
                self.SecurityQ_entry.current(0)

                SecurityA = Label(self.root2, text="Answer", font=("calibri", 15, "bold"), bg="white", fg="black")
                SecurityA.place(x=50, y=150)
                self.SecurityA_entry = ttk.Entry(self.root2, font=("calibri", 15))
                self.SecurityA_entry.place(x=50, y=180, width=250)

                newpasswd = Label(self.root2, text="New Password", font=("calibri", 15, "bold"), bg="white", fg="black")
                newpasswd.place(x=50, y=220)
                self.newpasswd_entry = ttk.Entry(self.root2, font=("calibri", 15))
                self.newpasswd_entry.place(x=50, y=250, width=250)

                btn = Button(self.root2, command=self.reset_password, text="Reset", font=("calibri", 15, "bold"),
                             fg="white", bg="blue")
                btn.place(x=100, y=290)




class Menupage:
    def __init__(self,root):
        self.root = root
        self.root.title("Home Menu Page")
        self.root.geometry('1600x900+0+0')

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\menubg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # f1 for patients
        f1 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f1.place(x=150, y=150, width=300, height=200)
        # buttons part
        img1 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu1.jpg")
        img1 = img1.resize((300, 200), Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        b1 = Button(f1, command= self.patient_window , image=self.photoimage1,  borderwidth=0, cursor="hand2")
        b1.place(x=0, y=0, width=300)
        name1 = Label(self.root, text="Patients ", font=("calibri", 15, "bold"), bg="white")
        name1.place(x=150, y=120)



        #f2 for doctors
        f2 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f2.place(x=600, y=150, width=300, height=200)
        img2 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu2.jpg")
        img2 = img2.resize((300, 200), Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        b2 = Button(f2,command= self.doctor_window , image=self.photoimage2, borderwidth=0, cursor="hand2")
        b2.place(x=0, y=0, width=300)
        name2 = Label(self.root, text="Doctors ", font=("calibri", 15, "bold"), bg="white")
        name2.place(x=600, y=120)



        #f3 for appointments
        f3 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f3.place(x=1075, y=150, width=300, height=200)
        img3 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu3.jpg")
        img3 = img3.resize((300, 200), Image.ANTIALIAS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        b3 = Button(f3,command= self.appointment_window , image=self.photoimage3, borderwidth=0, cursor="hand2")
        b3.place(x=0, y=0, width=300)
        name3 = Label(self.root, text="Appointments", font=("calibri", 15, "bold"), bg="white")
        name3.place(x=1075, y=120)




        #f5 for beds
        f5 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f5.place(x=150, y=450, width=300, height=200)
        img5 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu5.jpg")
        img5 = img5.resize((300, 200), Image.ANTIALIAS)
        self.photoimage5 = ImageTk.PhotoImage(img5)
        b5 = Button(f5,command= self.bed_window , image=self.photoimage5, borderwidth=0, cursor="hand2")
        b5.place(x=0, y=0, width=300)
        name5 = Label(self.root, text="Beds ", font=("calibri", 15, "bold"), bg="white")
        name5.place(x=150, y=420)


        #f6 for emergency
        f6 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f6.place(x=600, y=450, width=300, height=200)
        img6 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu6.jpg")
        img6 = img6.resize((300, 200), Image.ANTIALIAS)
        self.photoimage6 = ImageTk.PhotoImage(img6)
        b6 = Button(f6,command= self.emergency_window , image=self.photoimage6, borderwidth=0, cursor="hand2")
        b6.place(x=0, y=0, width=300)
        name6 = Label(self.root, text="Emergency ", font=("calibri", 15, "bold"), bg="white")
        name6.place(x=600, y=420)


        # #f7 for admin
        # f7 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        #
        # img7 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu7.jpg")
        # img7 = img7.resize((300, 200), Image.ANTIALIAS)
        # self.photoimage7 = ImageTk.PhotoImage(img7)
        # b7 = Button(f7, image=self.photoimage7, borderwidth=0, cursor="hand2")
        # b7.place(x=0, y=0, width=300)
        # name7 = Label(self.root, text="Admin ", font=("calibri", 15, "bold"), bg="white")


        #f4 for staffs
        f4 = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        f4.place(x=1075, y=450, width=300, height=200)
        img4 = Image.open(r"C:\Users\abhib\Desktop\21535001\images\menu4.jpg")
        img4 = img4.resize((300, 200), Image.ANTIALIAS)
        self.photoimage4 = ImageTk.PhotoImage(img4)
        b4 = Button(f4,command= self.staff_window , image=self.photoimage4, borderwidth=0, cursor="hand2")
        b4.place(x=0, y=0, width=300)
        name4 = Label(self.root, text="Staffs ", font=("calibri", 15, "bold"), bg="white")
        name4.place(x=1075, y=420)


    def appoint_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = appoint_Register(self.new_window)

    # declaring function to open individual windows
    def patient_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Patient(self.new_window)

    def doctor_window(self):
        self.new_window1 = Toplevel(self.root)
        self.app = Doctor(self.new_window1)

    def appointment_window(self):
        self.new_window2 = Toplevel(self.root)
        self.app = Appointment(self.new_window2)

    def staff_window(self):
        self.new_window3 = Toplevel(self.root)
        self.app = Staff(self.new_window3)

    def bed_window(self):
        self.new_window4 = Toplevel(self.root)
        self.app = Bed(self.new_window4)

    def emergency_window(self):
        self.new_window5 = Toplevel(self.root)
        self.app = Emergency(self.new_window5)


class Doctor:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Menu")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_doctorage = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_doctoremail = StringVar()
        self.var_address = StringVar()
        self.var_qualification = StringVar()
        self.var_department = StringVar()
        self.var_cabin = StringVar()
        self.var_joiningdate = StringVar()
        self.var_salary = StringVar()

        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\doctorbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.doctortable = ttk.Treeview(rowframe, column=(
        "DID", "First name", "Last name", "Age", "Gender", "Contact No", "Email", "Address", "Qualification",
        "Department", "Salary", "Status", "Cabin", "Joining date", "Resign date"), xscrollcommand=scroll_x.set,
                                        yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.doctortable.xview)
        scroll_y.config(command=self.doctortable.yview)

        self.doctortable.heading("DID", text="DID")
        self.doctortable.heading("First name", text="First name")
        self.doctortable.heading("Last name", text="Last name")
        self.doctortable.heading("Age", text="Age")
        self.doctortable.heading("Gender", text="Gender")
        self.doctortable.heading("Contact No", text="Contact No")
        self.doctortable.heading("Email", text="Email")
        self.doctortable.heading("Address", text="Address")
        self.doctortable.heading("Qualification", text="Qualification")
        self.doctortable.heading("Department", text="Department")
        self.doctortable.heading("Salary", text="Salary")
        self.doctortable.heading("Status", text="Status")
        self.doctortable.heading("Cabin", text="Cabin")
        self.doctortable.heading("Joining date", text="Joining date")
        self.doctortable.heading("Resign date", text="Resign date")

        self.doctortable["show"] = "headings"
        self.doctortable.column("DID", width=100)
        self.doctortable.column("First name", width=100)
        self.doctortable.column("Last name", width=100)
        self.doctortable.column("Age", width=100)
        self.doctortable.column("Gender", width=100)
        self.doctortable.column("Contact No", width=100)
        self.doctortable.column("Email", width=100)
        self.doctortable.column("Address", width=200)
        self.doctortable.column("Qualification", width=100)
        self.doctortable.column("Department", width=100)
        self.doctortable.column("Salary", width=100)
        self.doctortable.column("Status", width=100)
        self.doctortable.column("Cabin", width=100)
        self.doctortable.column("Joining date", width=100)
        self.doctortable.column("Resign date", width=100)

        self.doctortable.pack(fill=BOTH, expand=1)
        self.fetch_entries()

        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        registerdoctor = Button(topframe, command=self.doctor_register_window, text="Register doctor",
                                font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                                fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        registerdoctor.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe, command=self.update_doctor_window, text="Update doctor Details",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.discharge_doctor_window, text="Dismiss doctor",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=480, y=10, width=200, height=50)

        appointmentbyid = Button(topframe, command=self.appointmentby_id, text="Appointment by ID",
                                 font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                                 fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        appointmentbyid.place(x=710, y=10, width=200, height=50)

        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Doctor list:", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=950, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable=self.var_searchbydrop, font=("calibri", 15),
                                         state="readonly")
        self.searchbydrop["values"] = (
        "Select", "did", "firstname", "lastname", "gender", "age", "contact", "email", "address", "qualification",
        "status", "department", "salary", "cabin", "joiningdate", "resigndate")
        self.searchbydrop.place(x=1050, y=10, width=100)
        self.searchbydrop.current(0)

        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_searchbydropentry, font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command=self.searchbyfunction, text="Search", font=("calibri", 15, "bold"),
                            bd=2, relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)

        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        showallbutton = Button(botframe, command=self.fetch_entries, text="Show All", font=("calibri", 15, "bold"),
                               bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)

    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from doctor")
        data = my_cur.fetchall()
        if len(data) != 0:
            self.doctortable.delete(*self.doctortable.get_children())
            for i in data:
                self.doctortable.insert("", END, values=i)
                conn.commit()
            conn.close()

    def appointmentby_id(self):
        self.root6 = Toplevel()
        self.root6.title("Appointment by DID")
        self.root6.geometry('1100x500+250+100')

        # variables
        self.var_did = StringVar()

        # background image
        self.bg4 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\doctorbg.jpg")
        bg_label = Label(self.root6, image=self.bg4)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe1 = Frame(self.root6, bd=4, bg="white", relief=RIDGE)
        rowframe1.place(x=50, y=110, width=1000, height=350)

        scroll_x = ttk.Scrollbar(rowframe1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe1, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe1, column=(
            "Doctor ID", "Appointment Status", "Date", "Time", "Patient firstname", "Patient lastname",
            "Patient gender",
            "Patient bloodtype", "Admit date", "Symptoms", "Patient contact no", "Patient ID", "Appointment ID"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.appointtable.xview)
        scroll_y.config(command=self.appointtable.yview)
        # make channges here
        self.appointtable.heading("Doctor ID", text="Doctor ID")
        self.appointtable.heading("Appointment Status", text="Appointment Status")
        self.appointtable.heading("Date", text="Date")
        self.appointtable.heading("Time", text="Time")
        self.appointtable.heading("Patient firstname", text="Patient firstname")
        self.appointtable.heading("Patient lastname", text="Patient lastname")
        self.appointtable.heading("Patient gender", text="Patient gender")
        self.appointtable.heading("Patient bloodtype", text="Patient bloodtype")
        self.appointtable.heading("Admit date", text="Admit date")
        self.appointtable.heading("Symptoms", text="Symptoms")
        self.appointtable.heading("Patient contact no", text="Patient contact no")
        self.appointtable.heading("Patient ID", text="Patient ID")
        self.appointtable.heading("Appointment ID", text="Appointment ID")

        self.appointtable["show"] = "headings"
        self.appointtable.column("Doctor ID", width=100)
        self.appointtable.column("Appointment Status", width=100)
        self.appointtable.column("Date", width=100)
        self.appointtable.column("Time", width=100)
        self.appointtable.column("Patient firstname", width=100)
        self.appointtable.column("Patient lastname", width=100)
        self.appointtable.column("Patient gender", width=100)
        self.appointtable.column("Patient bloodtype", width=100)
        self.appointtable.column("Admit date", width=100)
        self.appointtable.column("Symptoms", width=100)
        self.appointtable.column("Patient contact no", width=100)
        self.appointtable.column("Patient ID", width=100)
        self.appointtable.column("Appointment ID", width=100)
        self.appointtable.pack(fill=BOTH, expand=1)

        ######################### button frame #########################

        # nav frame
        navframe1 = Frame(self.root6, bg="white")
        navframe1.place(x=50, y=50, width=1000, height=50)

        searchby = Label(navframe1, text="Enter Doctor ID :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=5, y=10)
        self.searchbar_entry = ttk.Entry(navframe1, textvariable=self.var_did, font=("calibri", 15))
        self.searchbar_entry.place(x=170, y=10, width=100)

        nsearchbtn = Button(navframe1, command=self.searchbyfunctionaid, text="Search", font=("calibri", 15, "bold"),
                            bd=2,
                            relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=290, y=10, width=100, height=30)


    def searchbyfunctionaid(self):
        if self.var_did.get() == "":
            messagebox.showerror("Error", "Please fill the field")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                query = "select distinct doctor.did,appointment.status , appointment.dates , appointment.timing , patient.firstname ,patient.lastname,patient.gender,patient.blood,patient.admitdate,patient.symptom , patient.contact , patient.pid , appointment.aid from appointment , patient , doctor where doctor.did =%s and appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted'"
                value = (int(self.var_did.get()),)
                my_cur.execute(query, value)
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root6)

    def update_doctor_window(self):
        self.root2 = Toplevel()
        self.root2.title("Update doctor Details")
        self.root2.geometry("850x550+400+50")

        # background image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\doctorbg.jpg")
        bg_label = Label(self.root2, image=self.bg1)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_did_update = StringVar()
        self.var_firstname_update = StringVar()
        self.var_lastname_update = StringVar()
        self.var_doctorage_update = StringVar()
        self.var_salary_update = StringVar()
        self.var_address_update = StringVar()
        self.var_email_update = StringVar()
        self.var_contact_update = StringVar()
        self.var_qualification_update = StringVar()
        self.var_cabin_update = StringVar()

        did_update = Label(self.root2, text="Enter valid DID ", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        did_update.place(x=150, y=80)
        self.did_update_entry = ttk.Entry(self.root2, textvariable=self.var_did_update, font=("calibri", 15))
        self.did_update_entry.place(x=150, y=110, width=250)

        firstname_update = Label(self.root2, text="First Name ", font=("calibri", 15, "bold"), bg="white",
                                 fg="black")
        firstname_update.place(x=450, y=80)  # 150
        self.firstname_update_entry = ttk.Entry(self.root2, textvariable=self.var_firstname_update,
                                                font=("calibri", 15))
        self.firstname_update_entry.place(x=450, y=110, width=250)  # 180

        doctorage_update = Label(self.root2, text="Age ", font=("calibri", 15, "bold"), bg="white", fg="black")
        doctorage_update.place(x=150, y=150)
        self.doctorage_update_entry = ttk.Entry(self.root2, textvariable=self.var_doctorage_update,
                                                font=("calibri", 15))
        self.doctorage_update_entry.place(x=150, y=180, width=250)

        lastname_update = Label(self.root2, text="Last name ", font=("calibri", 15, "bold"), bg="white", fg="black")
        lastname_update.place(x=450, y=150)
        self.lastname_update_entry = ttk.Entry(self.root2, textvariable=self.var_lastname_update,
                                               font=("calibri", 15))
        self.lastname_update_entry.place(x=450, y=180, width=250)

        salary_update = Label(self.root2, text="Enter salary", font=("calibri", 15, "bold"), bg="white", fg="black")
        salary_update.place(x=150, y=220)
        self.salary_update_entry = ttk.Entry(self.root2, textvariable=self.var_salary_update, font=("calibri", 15))
        self.salary_update_entry.place(x=150, y=250, width=250)

        address_update = Label(self.root2, text="Enter Address", font=("calibri", 15, "bold"), bg="white",
                               fg="black")
        address_update.place(x=450, y=220)
        self.address_update_entry = ttk.Entry(self.root2, textvariable=self.var_address_update,
                                              font=("calibri", 15))
        self.address_update_entry.place(x=450, y=250, width=250)

        email_update = Label(self.root2, text="Enter email", font=("calibri", 15, "bold"), bg="white",
                             fg="black")
        email_update.place(x=150, y=290)
        self.email_update_entry = ttk.Entry(self.root2, textvariable=self.var_email_update,
                                            font=("calibri", 15))
        self.email_update_entry.place(x=150, y=320, width=250)

        contact_update = Label(self.root2, text="Enter contact no", font=("calibri", 15, "bold"), bg="white",
                               fg="black")
        contact_update.place(x=450, y=290)
        self.contact_update_entry = ttk.Entry(self.root2, textvariable=self.var_contact_update,
                                              font=("calibri", 15))
        self.contact_update_entry.place(x=450, y=320, width=250)

        qualification_update = Label(self.root2, text="Enter Qualification", font=("calibri", 15, "bold"),
                                     bg="white",
                                     fg="black")
        qualification_update.place(x=150, y=360)
        self.qualification_update_entry = ttk.Combobox(self.root2, textvariable=self.var_qualification_update,
                                                       font=("calibri", 15), state="readonly")
        self.qualification_update_entry["values"] = (
            "Select", "MBBS", "MD", "MCH", "BDS", "BHMS", "BAMS")

        self.qualification_update_entry.place(x=150, y=390, width=250)
        self.qualification_update_entry.current(0)

        cabin_update = Label(self.root2, text="Enter cabin ", font=("calibri", 15, "bold"), bg="white",
                             fg="black")
        cabin_update.place(x=450, y=360)
        self.cabin_update_entry = ttk.Entry(self.root2, textvariable=self.var_cabin_update,
                                            font=("calibri", 15))
        self.cabin_update_entry.place(x=450, y=390, width=250)

        btn = Button(self.root2, text="Update", command=self.update_doctor, font=("calibri", 15, "bold"),
                     fg="white", bg="#1a75ff")
        btn.place(x=370, y=450, width=100)

    def update_doctor(self):
        # do update here
        if self.var_did_update.get() == "" or self.var_doctorage_update.get() == "" or self.var_firstname_update.get() == "" or self.var_lastname_update.get() == "" or self.var_address_update.get() == "" or self.var_contact_update.get() == "" or self.var_email_update.get() == "" or self.var_qualification_update.get() == "Select" or self.var_salary_update.get() == "" or self.var_cabin_update.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from doctor where did=%s "
            value = (self.var_did_update.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Enter the correct doctor ID", parent=self.root2)
            else:
                query = "update doctor set firstname=%s,lastname=%s,contact=%s,address=%s,email=%s,salary=%s , age=%s , qualification=%s , cabin=%s where did=%s"
                value = (self.var_firstname_update.get(),
                         self.var_lastname_update.get(),
                         int(self.var_contact_update.get()),
                         self.var_address_update.get(),
                         self.var_email_update.get(),
                         int(self.var_salary_update.get()),
                         self.var_doctorage_update.get(),
                         self.var_qualification_update.get(),
                         self.var_cabin_update.get(),
                         self.var_did_update.get())

                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "doctor data updated ", parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()

    def discharge_doctor_window(self):
        self.root3 = Toplevel()
        self.root3.title("Remove doctor")
        self.root3.geometry("600x300+500+25")

        # background image
        self.bg2 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\doctorbg.jpg")
        bg_label = Label(self.root3, image=self.bg2)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_resigndate = StringVar()
        self.var_did_resign = StringVar()

        pid_resign = Label(self.root3, text="DID ", font=("calibri", 15, "bold"), bg="white", fg="black")
        pid_resign.place(x=150, y=40)
        self.pid_resign_entry = ttk.Entry(self.root3, textvariable=self.var_did_resign, font=("calibri", 15))
        self.pid_resign_entry.place(x=150, y=70, width=250)

        resigndate = Label(self.root3, text="Enter Resign date ", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        resigndate.place(x=150, y=110)
        self.resigndate_entry = ttk.Entry(self.root3, textvariable=self.var_resigndate, font=("calibri", 15))
        self.resigndate_entry.place(x=150, y=140, width=250)

        btn_discharge = Button(self.root3, text="Submit ", command=self.discharge_doctor,
                               font=("calibri", 15, "bold"), fg="white", bg="#1a75ff")
        btn_discharge.place(x=150, y=180)

    def discharge_doctor(self):
        if self.var_did_resign.get() == "" or self.var_resigndate.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from doctor where did=%s "
            value = (self.var_did_resign.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Enter the correct doctor ID", parent=self.root3)
            else:
                query = "update doctor set status='resigned',resigndate=%s where did=%s"
                value = (self.var_resigndate.get(),
                         self.var_did_resign.get())

                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "doctor removed ", parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select" or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select * from doctor where " + str(self.var_searchbydrop.get()) + " LIKE '%" + str(
                    self.var_searchbydropentry.get()) + "%'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.doctortable.delete(*self.doctortable.get_children())
                    for i in data1:
                        self.doctortable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def doctor_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = doctor_Register(self.new_window)

class doctor_Register:
    def __init__(self, root):
        self.root = root
        self.root.title("doctor Registration")
        self.root.geometry('1600x900+0+0')

        # variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_doctorage = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_doctoremail = StringVar()
        self.var_address = StringVar()
        self.var_qualification = StringVar()
        self.var_department = StringVar()
        self.var_cabin = StringVar()
        self.var_joiningdate = StringVar()
        self.var_salary = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\doctorbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\docregister.jpg")
        bg1_label = Label(self.root, image=self.bg1)
        bg1_label.place(x=50, y=100, width=470, height=600)

        # main frame
        frame = Frame(self.root, bg="white")
        frame.place(x=520, y=100, width=800, height=600)

        # register here text
        register_lbl = Label(frame, text="Register here", font=("calibri", 25, "bold"), fg="green", bg="white")
        register_lbl.place(x=20, y=20)

        # =====================    label and entry part ===========================

        # first row
        firstname = Label(frame, text="First name", font=("calibri", 15, "bold"), bg="white")
        firstname.place(x=50, y=100)
        self.firstname_entry = ttk.Entry(frame, textvariable=self.var_firstname, font=("calibri", 15))
        self.firstname_entry.place(x=50, y=130, width=250)

        lastname = Label(frame, text="Last name", font=("calibri", 15, "bold"), bg="white")
        lastname.place(x=370, y=100)
        self.lastname_entry = ttk.Entry(frame, textvariable=self.var_lastname, font=("calibri", 15))
        self.lastname_entry.place(x=370, y=130, width=250)

        # second row
        Gender = Label(frame, text="Gender", font=("calibri", 15, "bold"), bg="white")
        Gender.place(x=50, y=170)
        self.Gender_entry = ttk.Combobox(frame, textvariable=self.var_gender, font=("calibri", 15),
                                         state="readonly")
        self.Gender_entry["values"] = ("Select", "Male", "Female", "Other")
        self.Gender_entry.place(x=50, y=200, width=250)
        self.Gender_entry.current(0)

        qualification = Label(frame, text="Qualification", font=("calibri", 15, "bold"), bg="white")
        qualification.place(x=370, y=170)
        self.qualification_entry = ttk.Combobox(frame, textvariable=self.var_qualification, font=("calibri", 15),
                                                state="readonly")
        self.qualification_entry["values"] = ("Select", "MBBS", "MD", "MCH", "BDS", "BHMS", "BAMS")
        self.qualification_entry.place(x=370, y=200, width=250)
        self.qualification_entry.current(0)

        # third row
        contact = Label(frame, text="Contact", font=("calibri", 15, "bold"), bg="white")
        contact.place(x=50, y=240)
        self.contact_entry = ttk.Entry(frame, textvariable=self.var_contact, font=("calibri", 15))
        self.contact_entry.place(x=50, y=270, width=250)

        doctorage = Label(frame, text="Age", font=("calibri", 15, "bold"), bg="white")
        doctorage.place(x=370, y=240)
        self.doctorage_entry = ttk.Entry(frame, textvariable=self.var_doctorage, font=("calibri", 15))
        self.doctorage_entry.place(x=370, y=270, width=250)

        # fourth row
        admitdate = Label(frame, text="Joining date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        admitdate.place(x=50, y=310)
        self.admitdate_entry = ttk.Entry(frame, textvariable=self.var_joiningdate, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=340, width=250)

        email = Label(frame, text="email ", font=("calibri", 15, "bold"), bg="white")
        email.place(x=370, y=310)
        self.email_entry = ttk.Entry(frame, textvariable=self.var_doctoremail, font=("calibri", 15))
        self.email_entry.place(x=370, y=340, width=250)

        # fifth row
        address = Label(frame, text="Address ", font=("calibri", 15, "bold"), bg="white")
        address.place(x=50, y=380)
        self.admitdate_entry = ttk.Entry(frame, textvariable=self.var_address, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=410, width=250)

        salary = Label(frame, text="Salary ", font=("calibri", 15, "bold"), bg="white")
        salary.place(x=370, y=380)
        self.salary_entry = ttk.Entry(frame, textvariable=self.var_salary, font=("calibri", 15))
        self.salary_entry.place(x=370, y=410, width=250)

        # row 6
        department = Label(frame, text="Department ", font=("calibri", 15, "bold"), bg="white")
        department.place(x=50, y=450)
        self.department_entry = ttk.Combobox(frame, textvariable=self.var_department, font=("calibri", 15),
                                             state="readonly")
        self.department_entry["values"] = (
        "Select", "General", "Gynaechology", "Dental", "Cardiology", "Neurology", "Dermatology", "Radiology",
        "Surgical")
        self.department_entry.place(x=50, y=480, width=250)
        self.department_entry.current(0)

        cabin = Label(frame, text="Cabin no", font=("calibri", 15, "bold"), bg="white")
        cabin.place(x=370, y=450)
        self.cabin_entry = ttk.Entry(frame, textvariable=self.var_cabin, font=("calibri", 15))
        self.cabin_entry.place(x=370, y=480, width=250)

        # row7
        # buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\21535001\images\submit.jpg")
        img = img.resize((200, 50), Image.ANTIALIAS)
        self.photoimage = ImageTk.PhotoImage(img)
        b1 = Button(frame, image=self.photoimage, command=self.registerdata, borderwidth=0, cursor="hand2")
        b1.place(x=250, y=530, width=200)

        ########### function declaration

    def registerdata(self):
        if self.var_firstname.get() == "" or self.var_cabin == "" or self.var_department == "Select" or self.var_qualification.get() == "Select" or self.var_doctoremail.get() == "" or self.var_salary.get() == "" or self.var_lastname.get() == "" or self.var_gender.get() == "Select" or self.var_address.get() == "" or self.var_joiningdate.get() == "" or self.var_doctorage.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")

        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            my_cur.execute(
                "insert into doctor (firstname,lastname,gender,qualification,contact,address,joiningdate,age,salary,email,department,cabin) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (self.var_firstname.get(),
                 self.var_lastname.get(),
                 self.var_gender.get(),
                 self.var_qualification.get(),
                 int(self.var_contact.get()),
                 self.var_address.get(),
                 self.var_joiningdate.get(),
                 int(self.var_doctorage.get()),
                 int(self.var_salary.get()),
                 self.var_doctoremail.get(),
                 self.var_department.get(),
                 self.var_cabin.get())
                )

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registered Succesfully")

class Appointment:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Menu")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_pid = StringVar()
        self.var_did = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\appointmentbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe, column=(
        "AppointmentID", "Status", "Date", "Time", "Patient firstname", "Patient lastname", "Patient contact no",
        "Doctor firstname", "Doctor lastname", "Doctor contact no", "Cabin no", "Department", "Patient ID",
        "Doctor ID"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.appointtable.xview)
        scroll_y.config(command=self.appointtable.yview)
        # make channges here
        self.appointtable.heading("AppointmentID", text="AppointmentID")
        self.appointtable.heading("Status", text="Status")
        self.appointtable.heading("Date", text="Date")
        self.appointtable.heading("Time", text="Time")
        self.appointtable.heading("Patient firstname", text="Patient firstname")
        self.appointtable.heading("Patient lastname", text="Patient lastname")
        self.appointtable.heading("Patient contact no", text="Patient contact no")
        self.appointtable.heading("Doctor firstname", text="Doctor firstname")
        self.appointtable.heading("Doctor lastname", text="Doctor lastname")
        self.appointtable.heading("Doctor contact no", text="Doctor contact no")
        self.appointtable.heading("Cabin no", text="Cabin no")
        self.appointtable.heading("Department", text="Department")
        self.appointtable.heading("Patient ID", text="Patient ID")
        self.appointtable.heading("Doctor ID", text="Doctor ID")

        self.appointtable["show"] = "headings"
        self.appointtable.column("AppointmentID", width=100)
        self.appointtable.column("Status", width=100)
        self.appointtable.column("Date", width=100)
        self.appointtable.column("Time", width=100)
        self.appointtable.column("Patient firstname", width=100)
        self.appointtable.column("Patient lastname", width=100)
        self.appointtable.column("Patient contact no", width=100)
        self.appointtable.column("Doctor firstname", width=100)
        self.appointtable.column("Doctor lastname", width=100)
        self.appointtable.column("Doctor contact no", width=100)
        self.appointtable.column("Cabin no", width=100)
        self.appointtable.column("Department", width=100)
        self.appointtable.column("Patient ID", width=100)
        self.appointtable.column("Doctor ID", width=100)

        self.appointtable.pack(fill=BOTH, expand=1)
        self.fetch_entries()

        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        updatepat = Button(topframe, command=self.book_appointment_window, text="Book appointment",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.cancel_appointment_window, text="Cancel Appointment",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=250, y=10, width=200, height=50)

        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Appointments :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=900, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable=self.var_searchbydrop, font=("calibri", 12),
                                         state="readonly")
        self.searchbydrop["values"] = (
        "Select", "appointment.aid", "appointment.pid", "appointment.did", "appointment.status",
        "appointment.dates", "appointment.timing", "patient.firstname", "patient.lastname", "doctor.firstname",
        "doctor.lastname", "doctor.cabin", "doctor.department")
        self.searchbydrop.place(x=1000, y=10, width=150, height=30)
        self.searchbydrop.current(0)

        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_searchbydropentry, font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command=self.searchbyfunction, text="Search", font=("calibri", 15, "bold"),
                            bd=2, relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)

        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        showallbutton = Button(botframe, command=self.fetch_entries, text="Show All", font=("calibri", 15, "bold"),
                               bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)

    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute(
            "select distinct  appointment.aid , appointment.status , appointment.dates , appointment.timing , patient.firstname , patient.lastname , patient.contact ,doctor.firstname , doctor.lastname , doctor.contact, doctor.cabin , doctor.department , appointment.pid ,appointment.did from appointment , patient , doctor where appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted'")
        data = my_cur.fetchall()
        if len(data) != 0:
            self.appointtable.delete(*self.appointtable.get_children())
            for i in data:
                self.appointtable.insert("", END, values=i)
                conn.commit()
            conn.close()

    def book_appointment_window(self):
        self.root2 = Toplevel()
        self.root2.title("Book appointment")
        self.root2.geometry("600x500+500+50")

        # background image
        self.bga = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\appointmentbg.jpg")
        bg_label = Label(self.root2, image=self.bga)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_pid = StringVar()
        self.var_did = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        pid = Label(self.root2, text="Enter Patient ID ", font=("calibri", 15, "bold"), bg="white", fg="black")
        pid.place(x=150, y=80)
        self.pid_entry = ttk.Entry(self.root2, textvariable=self.var_pid, font=("calibri", 15))
        self.pid_entry.place(x=150, y=110, width=300)

        did = Label(self.root2, text="Enter Doctor ID", font=("calibri", 15, "bold"), bg="white", fg="black")
        did.place(x=150, y=150)
        self.did_entry = ttk.Entry(self.root2, textvariable=self.var_did, font=("calibri", 15))
        self.did_entry.place(x=150, y=180, width=300)

        bdate = Label(self.root2, text="Booking date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white",
                      fg="black")
        bdate.place(x=150, y=220)
        self.bdate_entry = ttk.Entry(self.root2, textvariable=self.var_date, font=("calibri", 15))
        self.bdate_entry.place(x=150, y=250, width=300)

        btime = Label(self.root2, text="Booking time (HH:MM:SS)", font=("calibri", 15, "bold"), bg="white",
                      fg="black")
        btime.place(x=150, y=290)
        self.btime_entry = ttk.Entry(self.root2, textvariable=self.var_time,
                                     font=("calibri", 15))
        self.btime_entry.place(x=150, y=320, width=300)

        btn = Button(self.root2, text="Book", command=self.book_appointment, font=("calibri", 15, "bold"),
                     fg="white", bg="#1a75ff")
        btn.place(x=150, y=360)

    def book_appointment(self):
        # do update here
        if self.var_pid.get() == "" or self.var_did.get() == "" or self.var_date.get() == "" or self.var_time.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()

            query = "select patient.pid , doctor.did from  patient ,doctor where patient.pid = %s and doctor.did = %s and doctor.status ='employee' and patient.status = 'Admitted'"
            value = (int(self.var_pid.get()), int(self.var_did.get()))
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Enter valid IDs", parent=self.root2)
            else:
                query = "insert into appointment (pid,did,dates,timing) values (%s,%s,%s,%s)"
                value = (int(self.var_pid.get()),
                         int(self.var_did.get()),
                         self.var_date.get(),
                         self.var_time.get())
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Booking Confirmed ", parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()

    def cancel_appointment_window(self):
        self.root3 = Toplevel()
        self.root3.title("Cancel appointment")
        self.root3.geometry("600x500+500+25")

        # background image
        self.bgb = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\appointmentbg.jpg")
        bg_label = Label(self.root3, image=self.bgb)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_canceldate = StringVar()
        self.var_aid_cancel = StringVar()
        self.var_bookingtime = StringVar()

        pid_resign = Label(self.root3, text="Enter appointment ID ", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        pid_resign.place(x=150, y=40)
        self.pid_resign_entry = ttk.Entry(self.root3, textvariable=self.var_aid_cancel, font=("calibri", 15))
        self.pid_resign_entry.place(x=150, y=70, width=250)

        resigndate = Label(self.root3, text="Enter booked date ", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        resigndate.place(x=150, y=110)
        self.resigndate_entry = ttk.Entry(self.root3, textvariable=self.var_canceldate, font=("calibri", 15))
        self.resigndate_entry.place(x=150, y=140, width=250)

        resigntime = Label(self.root3, text="Enter booked time", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        resigntime.place(x=150, y=180)
        self.resigntime_entry = ttk.Entry(self.root3, textvariable=self.var_bookingtime, font=("calibri", 15))
        self.resigntime_entry.place(x=150, y=210, width=250)

        btn_discharge = Button(self.root3, text="Cancel ", command=self.cancel_appointment,
                               font=("calibri", 15, "bold"), fg="white", bg="#1a75ff")
        btn_discharge.place(x=250, y=300)

    def cancel_appointment(self):
        if self.var_aid_cancel.get() == "" or self.var_canceldate.get() == "" or self.var_bookingtime.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from appointment where aid=%s and dates=%s and timing=%s "
            value = (self.var_aid_cancel.get(), self.var_canceldate.get(), self.var_bookingtime.get())
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root3)
            else:
                query = "update appointment set status='cancelled' where aid=%s"
                value = (self.var_aid_cancel.get(),)
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Appointment cancelled ", parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select" or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute(
                    "select distinct  appointment.aid , appointment.status , appointment.dates , appointment.timing , patient.firstname , patient.lastname , patient.contact ,doctor.firstname , doctor.lastname , doctor.contact, doctor.cabin , doctor.department , appointment.pid ,appointment.did from appointment , patient , doctor where appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted' and " + str(
                        self.var_searchbydrop.get()) + " = '" + str(self.var_searchbydropentry.get()) + "'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)



# def main():
#     win = Tk()
#     app = Emergency(win)
#     win.mainloop()


class Emergency:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Menu")
        self.root.geometry('1500x790+0+0')

        # variables

        self.var_did = StringVar()
        self.var_date = StringVar()


        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\emergencybg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe, column=(
        "Emergency Table ID", "Serving Date","Doctor ID","Doctor firstname", "Doctor lastname",
        "Cabin no", "Department", "Qualification" , "Contact no","Email ID" , "Status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.appointtable.xview)
        scroll_y.config(command=self.appointtable.yview)
        # make channges here
        self.appointtable.heading("Emergency Table ID", text="Emergency Table ID")
        self.appointtable.heading("Serving Date", text="Serving Date")
        self.appointtable.heading("Doctor ID", text="Doctor ID")
        self.appointtable.heading("Doctor firstname", text="Doctor firstname")
        self.appointtable.heading("Doctor lastname", text="Doctor lastname")
        self.appointtable.heading("Cabin no", text="Cabin no")
        self.appointtable.heading("Department", text="Department")
        self.appointtable.heading("Qualification", text="Qualification")
        self.appointtable.heading("Contact no", text="Doctor contact no")
        self.appointtable.heading("Email ID", text="Email ID")
        self.appointtable.heading("Status", text="Status")

        self.appointtable["show"] = "headings"
        self.appointtable.column("Emergency Table ID", width=100)
        self.appointtable.column("Serving Date", width=100)
        self.appointtable.column("Doctor ID", width=100)
        self.appointtable.column("Doctor firstname", width=100)
        self.appointtable.column("Doctor lastname", width=100)
        self.appointtable.column("Cabin no", width=100)
        self.appointtable.column("Department", width=100)
        self.appointtable.column("Qualification", width=100)
        self.appointtable.column("Contact no", width=100)
        self.appointtable.column("Email ID", width=100)
        self.appointtable.column("Status", width=100)


        self.appointtable.pack(fill=BOTH, expand=1)
        self.fetch_entries()

        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        updatepat = Button(topframe, command=self.addduty_window, text="Add new duty",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.reschedule_duty_window, text="Reschedule duty",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=250, y=10, width=200, height=50)

        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Emergency duties :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=900, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable=self.var_searchbydrop, font=("calibri", 12),
                                         state="readonly")
        self.searchbydrop["values"] = (
        "Select", "emergency.eid", "emergency.date", "emergency.did","doctor.firstname", "doctor.lastname", "doctor.cabin", "doctor.department",
        "doctor.qualification", "doctor.contact", "doctor.email",
        "emergency.status")
        self.searchbydrop.place(x=1000, y=10, width=150, height=30)
        self.searchbydrop.current(0)

        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_searchbydropentry, font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command=self.searchbyfunction, text="Search", font=("calibri", 15, "bold"), bd=2,
                            relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)

        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        showallbutton = Button(botframe, command=self.fetch_entries, text="Show All", font=("calibri", 15, "bold"),
                               bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)



    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select emergency.eid , emergency.date , doctor.did , doctor.firstname , doctor.lastname , doctor.cabin , doctor.department , doctor.qualification , doctor.contact , doctor.email , emergency.status from emergency , doctor  where emergency.did = doctor.did and doctor.status = 'employee' ")
        data = my_cur.fetchall()
        if len(data) != 0:
            self.appointtable.delete(*self.appointtable.get_children())
            for i in data:
                self.appointtable.insert("", END, values=i)
                conn.commit()
            conn.close()


    def addduty_window(self):
        self.root2 = Toplevel()
        self.root2.title("Add emergency duty")
        self.root2.geometry("600x500+500+50")

        # background image
        self.bga = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\emergencybg.jpg")
        bg_label = Label(self.root2, image=self.bga)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_did = StringVar()
        self.var_date = StringVar()

        did = Label(self.root2, text="Enter Doctor ID", font=("calibri", 15, "bold"), bg="white", fg="black")
        did.place(x=150, y=150)
        self.did_entry = ttk.Entry(self.root2, textvariable=self.var_did, font=("calibri", 15))
        self.did_entry.place(x=150, y=180, width=300)

        bdate = Label(self.root2, text="Enter Duty date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white", fg="black")
        bdate.place(x=150, y=220)
        self.bdate_entry = ttk.Entry(self.root2, textvariable=self.var_date, font=("calibri", 15))
        self.bdate_entry.place(x=150, y=250, width=300)

        btn = Button(self.root2, text="Schedule", command=self.addduty, font=("calibri", 15, "bold"), fg="white",
                     bg="#1a75ff")
        btn.place(x=150, y=360)


    def addduty(self):
        # do update here
        if self.var_did.get() == "" or self.var_date.get() == "" :
            messagebox.showerror("Error", "Please fill all the fields")

        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select doctor.did from doctor where doctor.did = %s and doctor.status ='employee' "
            value = (int(self.var_did.get()),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Enter valid IDs", parent=self.root2)
            else:
                query = "insert into emergency (did,date) values (%s,%s)"
                value = (int(self.var_did.get()), self.var_date.get())
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Duty added ", parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()


    def reschedule_duty_window(self):
        self.root3 = Toplevel()
        self.root3.title("Reschedule duty")
        self.root3.geometry("600x500+500+25")

        # background image
        self.bg4 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\emergencybg.jpg")
        bg_label = Label(self.root3, image=self.bg4)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_date = StringVar()
        self.var_eid = StringVar()  #using as EID
        self.var_did = StringVar()
        self.var_actualdate = StringVar()


        did_reschedule = Label(self.root3, text="Enter doctor ID ", font=("calibri", 15, "bold"), bg="white",
                           fg="black")
        did_reschedule.place(x=150, y=40)
        self.did_reschedule_entry = ttk.Entry(self.root3, textvariable=self.var_did, font=("calibri", 15))
        self.did_reschedule_entry.place(x=150, y=70, width=250)


        eid_reschedule = Label(self.root3, text="Enter emergency ID ", font=("calibri", 15, "bold"), bg="white",
                               fg="black")
        eid_reschedule.place(x=150, y=110)
        self.eid_reschedule_entry = ttk.Entry(self.root3, textvariable=self.var_eid, font=("calibri", 15))
        self.eid_reschedule_entry.place(x=150, y=140, width=250)


        date_actual = Label(self.root3, text="Actual date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white",
                                fg="black")
        date_actual.place(x=150, y=180)
        self.date_actual_entry = ttk.Entry(self.root3, textvariable=self.var_actualdate, font=("calibri", 15))
        self.date_actual_entry.place(x=150, y=210, width=250)


        date_reschedule = Label(self.root3, text="Rescheduled date(YYYY-MM-DD) ", font=("calibri", 15, "bold"), bg="white", fg="black")
        date_reschedule.place(x=150, y=250)
        self.date_reschedule_entry = ttk.Entry(self.root3, textvariable=self.var_date, font=("calibri", 15))
        self.date_reschedule_entry.place(x=150, y=280, width=250)


        btn_discharge = Button(self.root3, text=" Reschedule ", command=self.reschedule_duty,
                               font=("calibri", 15, "bold"), fg="white", bg="#1a75ff")
        btn_discharge.place(x=250, y=320)


    def reschedule_duty(self):
        if self.var_eid.get() == "" or self.var_date.get() == "" or self.var_did.get() == "" or self.var_actualdate.get() =="":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from emergency where did=%s and eid=%s and NOT date=%s  "
            value = (int(self.var_did.get()), int(self.var_eid.get()), self.var_date.get())
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root3)
            else:
                query = "update emergency set status ='rescheduled' , date=%s where eid=%s"
                value = ( self.var_date.get(),int(self.var_eid.get()))
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Emergency duty rescheduled ", parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select" or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()

                my_cur.execute("select emergency.eid , emergency.date , doctor.did , doctor.firstname , doctor.lastname , doctor.cabin , doctor.department , doctor.qualification , doctor.contact , doctor.email , emergency.status from emergency , doctor  where emergency.did = doctor.did and doctor.status = 'employee' and "+ str(self.var_searchbydrop.get()) + " = '" + str(self.var_searchbydropentry.get()) + "'")

                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def appoint_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = appoint_Register(self.new_window)


class Bed:
    def __init__(self, root):
        self.root = root
        self.root.title("Bed Menu")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_pid = StringVar()
        self.var_did = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\bedbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe, column=("Bed ID" , "Type" ,"Cost","Ward no","Allotted status" , "Patient ID" , "From date" ,"No of days" , "Final cost"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.appointtable.xview)
        scroll_y.config(command=self.appointtable.yview)
        # make channges here
        self.appointtable.heading("Bed ID", text="Bed ID")
        self.appointtable.heading("Type", text="Type")
        self.appointtable.heading("Cost", text="Cost")
        self.appointtable.heading("Ward no", text="Ward no")
        self.appointtable.heading("Allotted status", text="Allotted status")
        self.appointtable.heading("Patient ID", text="Patient ID")
        self.appointtable.heading("From date", text="From date")
        self.appointtable.heading("No of days", text="No of days")
        self.appointtable.heading("Final cost", text="Final cost")


        self.appointtable["show"] = "headings"
        self.appointtable.column("Bed ID", width=100)
        self.appointtable.column("Type", width=100)
        self.appointtable.column("Cost", width=100)
        self.appointtable.column("Ward no", width=100)
        self.appointtable.column("Allotted status", width=100)
        self.appointtable.column("Patient ID", width=100)
        self.appointtable.column("From date", width=100)
        self.appointtable.column("No of days", width=100)
        self.appointtable.column("Final cost", width=100)

        self.appointtable.pack(fill=BOTH, expand=1)
        self.fetch_entries()

        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        updatepat = Button(topframe, command=self.add_bed_window, text="Add New Bed",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.set_bedcost_window, text="Set Bed Cost",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=250, y=10, width=200, height=50)

        deletebed = Button(topframe, command=self.delete_bed_window, text="Delete Bed", font=("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        deletebed.place(x=480, y=10, width=200, height=50)

        allotbed = Button(topframe, command=self.allot_bed_window, text="Allot bed",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="#1a75ff",
                           activeforeground="white", activebackground="#1a75ff")
        allotbed.place(x=710, y=10, width=200, height=50)



        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Beds list :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=900, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable=self.var_searchbydrop, font=("calibri", 12),
                                         state="readonly")
        self.searchbydrop["values"] = ("Select" ,"bid" , "type" ,"cost","ward" ,"alloted","pid","fromdate")
        self.searchbydrop.place(x=1000, y=10, width=150, height=30)
        self.searchbydrop.current(0)

        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_searchbydropentry, font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command=self.searchbyfunction, text="Search", font=("calibri", 15, "bold"), bd=2,
                            relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)

        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        showallbutton = Button(botframe, command=self.fetch_entries, text="Show All", font=("calibri", 15, "bold"),
                               bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)


    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from bed")
        data = my_cur.fetchall()
        if len(data) != 0:
            self.appointtable.delete(*self.appointtable.get_children())
            for i in data:
                self.appointtable.insert("", END, values=i)
                conn.commit()
            conn.close()

    def delete_bed_window(self):
        self.root2 = Toplevel()
        self.root2.title("Delete Bed")
        self.root2.geometry("600x500+500+50")

        # declare variables
        self.var_bedid = StringVar()

        # background image
        self.bga = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\bedbg.jpg")
        bg_label = Label(self.root2, image=self.bga)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        bedid = Label(self.root2, text="Enter Bed ID", font=("calibri", 15, "bold"), bg="white", fg="black")
        bedid.place(x=150, y=150)
        self.bedid_entry = ttk.Entry(self.root2, textvariable=self.var_bedid, font=("calibri", 15))
        self.bedid_entry.place(x=150, y=180, width=300)


        btn = Button(self.root2, text="Delete", command=self.delete_bed, font=("calibri", 15, "bold"), fg="white",
                     bg="#1a75ff")
        btn.place(x=150, y=360)


    def delete_bed(self):
        # do update here
        if self.var_bedid.get() == ""  :
            messagebox.showerror("Error", "Please fill the ID")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from bed where bid=%s and alloted='no'"
            value = (self.var_bedid.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root2)
            else:
                query = "delete from bed where bid=%s and alloted='no'"
                value = (int(self.var_bedid.get()),)
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Deleted bed", parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()


    def add_bed_window(self):
        self.root2 = Toplevel()
        self.root2.title("Add Bed")
        self.root2.geometry("600x500+500+50")

        # declare variables
        self.var_btype = StringVar()
        self.var_wardno = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()

        # background image
        self.bgb = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\bedbg.jpg")
        bg_label = Label(self.root2, image=self.bgb)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        btype = Label(self.root2, text="Enter Bed type ", font=("calibri", 15, "bold"), bg="white", fg="black")
        btype.place(x=150, y=80)
        self.btype_entry = ttk.Combobox(self.root2, textvariable=self.var_btype, font=("calibri", 15),state="readonly")
        self.btype_entry["values"] = ("Select", "General","Semi Electric","Electric","ICU")
        self.btype_entry.place(x=150, y=110, width=300)
        self.btype_entry.current(0)

        wardno = Label(self.root2, text="Enter ward no", font=("calibri", 15, "bold"), bg="white", fg="black")
        wardno.place(x=150, y=150)
        self.wardno_entry = ttk.Entry(self.root2, textvariable=self.var_wardno, font=("calibri", 15))
        self.wardno_entry.place(x=150, y=180, width=300)


        btn = Button(self.root2, text="Add", command=self.add_bed, font=("calibri", 15, "bold"), fg="white",
                     bg="#1a75ff")
        btn.place(x=150, y=360)


    def add_bed(self):
        # do update here
        if self.var_btype.get() == "" or self.var_wardno.get() == "Select" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "insert into bed (type,ward) values (%s,%s)"
            value = (self.var_btype.get() , self.var_wardno.get())
            my_cur.execute(query, value)
            conn.commit()
            conn.close()
            messagebox.showinfo("Info", "Bed added ", parent=self.root2)
            self.fetch_entries()
            self.root2.destroy()

    def set_bedcost_window(self):
        self.root3 = Toplevel()
        self.root3.title("Set bed cost")
        self.root3.geometry("600x500+500+25")

        # declare variables
        self.var_btype = StringVar()
        self.var_setcost = StringVar()

        # background image
        self.bgc = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\bedbg.jpg")
        bg_label = Label(self.root3, image=self.bgc)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        btype = Label(self.root3, text="Enter Bed type ", font=("calibri", 15, "bold"), bg="white", fg="black")
        btype.place(x=150, y=40)
        self.btype_entry = ttk.Combobox(self.root3, textvariable=self.var_btype, font=("calibri", 15), state="readonly")
        self.btype_entry["values"] = ("Select", "General", "Semi Electric", "Electric", "ICU")
        self.btype_entry.place(x=150, y=70, width=300)
        self.btype_entry.current(0)

        set_cost = Label(self.root3, text="Cost ", font=("calibri", 15, "bold"), bg="white", fg="black")
        set_cost.place(x=150, y=110)
        self.set_cost_entry = ttk.Entry(self.root3, textvariable=self.var_setcost, font=("calibri", 15))
        self.set_cost_entry.place(x=150, y=140, width=250)

        btn_set = Button(self.root3, text="Set", command=self.cancel_appointment,
                               font=("calibri", 15, "bold"), fg="white", bg="#1a75ff")
        btn_set.place(x=250, y=300)

    def cancel_appointment(self):
        if self.var_btype.get() == "Select" or self.var_setcost.get() == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from bed where type=%s "
            value = (self.var_btype.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchall()
            if row == None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root3)
            else:
                query = "update bed set cost=%s where type=%s"
                value = (int(self.var_setcost.get()),self.var_btype.get())
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Cost set successfully", parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()



    def allot_bed_window(self):
        self.root4 = Toplevel()
        self.root4.title("Bed allotment")
        self.root4.geometry("600x500+500+25")

        # background image
        self.bgd = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\bedbg.jpg")
        bg_label = Label(self.root4, image=self.bgd)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # declare variables
        self.var_pid = StringVar()
        self.var_bid = StringVar()
        self.var_fromdate = StringVar()
        self.var_days = StringVar()
        self.var_btype = StringVar()

        pid = Label(self.root4, text="Enter PID ", font=("calibri", 15, "bold"), bg="white", fg="black")
        pid.place(x=150, y=40)
        self.pid_entry = ttk.Entry(self.root4, textvariable=self.var_pid, font=("calibri", 15))
        self.pid_entry.place(x=150, y=70, width=250)

        btype = Label(self.root4, text="Enter Bed type ", font=("calibri", 15, "bold"), bg="white", fg="black")
        btype.place(x=150, y=110)
        self.btype_entry = ttk.Combobox(self.root4, textvariable=self.var_btype, font=("calibri", 15), state="readonly")
        self.btype_entry["values"] = ("Select", "General", "Semi Electric", "Electric", "ICU")
        self.btype_entry.place(x=150, y=140, width=250)
        self.btype_entry.current(0)


        bid = Label(self.root4, text="Enter BID ", font=("calibri", 15, "bold"), bg="white", fg="black")
        bid.place(x=150, y=180)
        self.bid_entry = ttk.Entry(self.root4, textvariable=self.var_bid, font=("calibri", 15))
        self.bid_entry.place(x=150, y=210, width=250)

        fromdate = Label(self.root4, text="From date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white", fg="black")
        fromdate.place(x=150, y=250)
        self.fromdate_entry = ttk.Entry(self.root4, textvariable=self.var_fromdate, font=("calibri", 15))
        self.fromdate_entry.place(x=150, y=280, width=250)

        days = Label(self.root4, text="No. of days ", font=("calibri", 15, "bold"), bg="white", fg="black")
        days.place(x=150, y=320)
        self.days_entry = ttk.Entry(self.root4, textvariable=self.var_days, font=("calibri", 15))
        self.days_entry.place(x=150, y=350, width=250)


        btn_set = Button(self.root4, text="Allot", command=self.allot_bed,
                               font=("calibri", 15, "bold"), fg="white", bg="#1a75ff")
        btn_set.place(x=250, y=390)


    def allot_bed(self):
        if self.var_btype.get() == "Select" or self.var_bid.get() == "" or self.var_pid.get()=="" or self.var_fromdate.get()=="" or self.var_days.get()==""  :
            messagebox.showerror("Error", "Please fill all the fields")

        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from bed , patient where bed.bid =%s and bed.type = %s and patient.pid = %s and bed.alloted='no' and patient.status = 'Admitted' ; "
            value = (int(self.var_bid.get()) ,self.var_btype.get(),int(self.var_pid.get()))
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root4)
            else:
                query = "update bed set pid=%s , alloted='yes' , fromdate=%s ,days=%s , finalcost= cost* %s where bid=%s"
                value = (int(self.var_pid.get()),self.var_fromdate.get() , int(self.var_days.get()) ,int(self.var_days.get()) ,int(self.var_bid.get()) )
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Bed alloted successfully", parent=self.root4)
                self.fetch_entries()
                self.root4.destroy()


    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select" or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select * from bed where " + str(self.var_searchbydrop.get()) + " = " + "'" + str(self.var_searchbydropentry.get()) + "'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def appoint_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = appoint_Register(self.new_window)


class Staff:
    def __init__(self,root):
        self.root = root
        self.root.title("Staff Menu")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_gender = StringVar()
        self.var_staffage = StringVar()
        self.var_staffemail = StringVar()
        self.var_contact = StringVar()
        self.var_address = StringVar()
        self.var_status = StringVar()
        self.var_type = StringVar()
        self.var_salary = StringVar()


        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()


        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\staffbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4 ,bg="white" , relief = RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450 )

        scroll_x = ttk.Scrollbar(rowframe,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.stafftable=ttk.Treeview(rowframe , column=("SID" , "First name","Last name","Gender" ,"Age", "Contact No" ,"Email" ,"Address" , "Status" ,"Type" ,"Salary" ,"Joining date" , "Resign date"),xscrollcommand=scroll_x.set , yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM ,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.stafftable.xview)
        scroll_y.config(command=self.stafftable.yview)

        self.stafftable.heading("SID",text="SID")
        self.stafftable.heading("First name", text="First name")
        self.stafftable.heading("Last name", text="Last name")
        self.stafftable.heading("Gender", text="Gender")
        self.stafftable.heading("Age", text="Age")
        self.stafftable.heading("Contact No", text="Contact No")
        self.stafftable.heading("Email", text="Email")
        self.stafftable.heading("Address", text="Address")
        self.stafftable.heading("Status", text="Status")
        self.stafftable.heading("Type", text="Type")
        self.stafftable.heading("Salary", text="Salary")
        self.stafftable.heading("Joining date", text="Joining date")
        self.stafftable.heading("Resign date", text="Resign date")


        self.stafftable["show"]="headings"
        self.stafftable.column("SID",width=100)
        self.stafftable.column("First name", width=100)
        self.stafftable.column("Last name", width=100)
        self.stafftable.column("Gender", width=100)
        self.stafftable.column("Age", width=100)
        self.stafftable.column("Contact No", width=100)
        self.stafftable.column("Email", width=100)
        self.stafftable.column("Address", width=200)
        self.stafftable.column("Status", width=100)
        self.stafftable.column("Type", width=100)
        self.stafftable.column("Salary", width=100)
        self.stafftable.column("Joining date", width=100)
        self.stafftable.column("Resign date", width=100)

        self.stafftable.pack(fill=BOTH,expand=1)
        self.fetch_entries()


        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        registerstaff = Button(topframe,command=self.staff_register_window, text="Register New Staff", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        registerstaff.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe,command = self.update_staff_window, text="Update staff Details", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.discharge_staff_window ,  text="Dismiss staff", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=480, y=10, width=200, height=50)



        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Staff :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=950, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable = self.var_searchbydrop , font=("calibri", 15), state="readonly")
        self.searchbydrop["values"] = ("Select", "sid", "firstname", "lastname", "gender", "age",  "contact", "email", "address" ,"status" , "type","salary" ,"joiningdate","resigndate")
        self.searchbydrop.place(x=1050, y=10, width=100)
        self.searchbydrop.current(0)


        self.searchbar_entry = ttk.Entry(navframe,  textvariable = self.var_searchbydropentry , font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command = self.searchbyfunction ,  text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)


        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)


        showallbutton = Button(botframe, command= self.fetch_entries ,  text="Show All", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                          fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)


    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from staff")
        data=my_cur.fetchall()
        if len(data)!=0:
            self.stafftable.delete(*self.stafftable.get_children())
            for i in data:
                self.stafftable.insert("",END,values=i)
                conn.commit()
            conn.close()




    def update_staff_window(self) :
                self.root2=Toplevel()
                self.root2.title("Update staff Details")
                self.root2.geometry("600x750+500+50")

                # background image
                self.bg3 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\staffbg.jpg")
                bg_label = Label(self.root2, image=self.bg3)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                #declare variables
                self.var_sid_update = StringVar()
                self.var_firstname_update = StringVar()
                self.var_lastname_update = StringVar()
                self.var_staffage_update = StringVar()
                self.var_salary_update = StringVar()
                self.var_address_update = StringVar()
                self.var_email_update = StringVar()
                self.var_contact_update = StringVar()



                sid_update = Label(self.root2, text="SID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                sid_update.place(x=150, y=80)
                self.sid_update_entry = ttk.Entry(self.root2, textvariable=self.var_sid_update, font=("calibri", 15))
                self.sid_update_entry.place(x=150, y=110, width=250)

                firstname_update = Label(self.root2, text="First Name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                firstname_update.place(x=150, y=150)
                self.firstname_update_entry = ttk.Entry(self.root2,textvariable = self.var_firstname_update, font=("calibri", 15))
                self.firstname_update_entry.place(x=150, y=180, width=250)

                lastname_update = Label(self.root2, text="Last name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                lastname_update.place(x=150, y=220)
                self.lastname_update_entry = ttk.Entry(self.root2, textvariable = self.var_lastname_update, font=("calibri", 15))
                self.lastname_update_entry.place(x=150, y=250, width=250)


                staffage_update = Label(self.root2, text="Age ", font=("calibri", 15, "bold"), bg="white", fg="black")
                staffage_update.place(x=150, y=290)
                self.staffage_update_entry = ttk.Entry(self.root2, textvariable=self.var_staffage_update,
                                                  font=("calibri", 15))
                self.staffage_update_entry.place(x=150, y=320, width=250)


                salary_update = Label(self.root2, text="Enter salary", font=("calibri", 15, "bold"), bg="white", fg="black")
                salary_update.place(x=150, y=360)
                self.salary_update_entry = ttk.Entry(self.root2,textvariable = self.var_salary_update, font=("calibri", 15))
                self.salary_update_entry.place(x=150, y=390, width=250)


                address_update = Label(self.root2, text="Enter Address", font=("calibri", 15, "bold"), bg="white",
                                        fg="black")
                address_update.place(x=150, y=430)
                self.address_update_entry = ttk.Entry(self.root2,textvariable = self.var_address_update, font=("calibri", 15))
                self.address_update_entry.place(x=150, y=460, width=250)

                email_update = Label(self.root2, text="Enter email", font=("calibri", 15, "bold"), bg="white",
                                       fg="black")
                email_update.place(x=150, y=500)
                self.email_update_entry = ttk.Entry(self.root2, textvariable=self.var_email_update,
                                                      font=("calibri", 15))
                self.email_update_entry.place(x=150, y=530, width=250)


                contact_update = Label(self.root2, text="Enter contact no", font=("calibri", 15, "bold"), bg="white" ,fg="black")
                contact_update.place(x=150, y=570)
                self.contact_update_entry = ttk.Entry(self.root2,textvariable = self.var_contact_update, font=("calibri", 15))
                self.contact_update_entry.place(x=150, y=600, width=250)

                btn=Button(self.root2, text="Update" , command = self.update_staff,font=("calibri", 15,"bold") , fg="white",bg="#1a75ff")
                btn.place(x=150,y=640)



    def update_staff(self):
        #do update here
        if self.var_sid_update.get() == "" or self.var_staffage_update.get() == "" or self.var_firstname_update.get() == "" or self.var_lastname_update.get() == "" or self.var_address_update.get() == "" or self.var_contact_update.get()=="" or self.var_email_update.get() == ""  or self.var_salary_update.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from staff where sid=%s "
            value = (self.var_sid_update.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct staff ID", parent=self.root2)
            else :
                query = "update staff set firstname=%s,lastname=%s,contact=%s,address=%s,email=%s,salary=%s , age=%s where sid=%s"
                value = (self.var_firstname_update.get() ,
                         self.var_lastname_update.get() ,
                         int(self.var_contact_update.get()) ,
                         self.var_address_update.get() ,
                         self.var_email_update.get() ,
                         int(self.var_salary_update.get()),
                         self.var_staffage_update.get(),
                         self.var_sid_update.get())

                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "staff data updated " , parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()

    def discharge_staff_window(self) :
                self.root3=Toplevel()
                self.root3.title("Remove staff")
                self.root3.geometry("600x300+500+25")

                # background image
                self.bg7 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\staffbg.jpg")
                bg_label = Label(self.root3, image=self.bg7)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                #declare variables
                self.var_resigndate = StringVar()
                self.var_sid_resign = StringVar()

                pid_resign = Label(self.root3, text="SID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                pid_resign.place(x=150, y=40)
                self.pid_resign_entry = ttk.Entry(self.root3, textvariable=self.var_sid_resign, font=("calibri", 15))
                self.pid_resign_entry.place(x=150, y=70, width=250)

                resigndate= Label(self.root3, text="Enter Resign date ", font=("calibri", 15, "bold"), bg="white", fg="black")
                resigndate.place(x=150, y=110)
                self.resigndate_entry = ttk.Entry(self.root3,textvariable = self.var_resigndate ,font=("calibri", 15))
                self.resigndate_entry.place(x=150, y=140, width=250)

                btn_discharge=Button(self.root3, text="Submit " , command = self.discharge_staff,font=("calibri", 15,"bold") , fg="white",bg="#1a75ff")
                btn_discharge.place(x=150,y=180)

    def discharge_staff(self):
        if self.var_sid_resign.get() == ""  or self.var_resigndate.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from staff where sid=%s "
            value = (self.var_sid_resign.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct staff ID", parent=self.root3)
            else :
                query = "update staff set status='resigned',leavingdate=%s where sid=%s"
                value = (self.var_resigndate.get() ,
                         self.var_sid_resign.get())


                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "staff removed " , parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select"  or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select * from staff where " + str(self.var_searchbydrop.get()) + " LIKE '%" + str(self.var_searchbydropentry.get())+ "%'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.stafftable.delete(*self.stafftable.get_children())
                    for i in data1:
                        self.stafftable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error" , f"Due To:{str(es)}",parent=self.root)

    def staff_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = staff_Register(self.new_window)



class staff_Register:
    def __init__(self,root):
        self.root = root
        self.root.title("staff Registration")
        self.root.geometry('1600x900+0+0')

        #variables
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_gender = StringVar()
        self.var_age = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_address = StringVar()
        self.var_type = StringVar()
        self.var_salary = StringVar()
        self.var_joiningdate = StringVar()



        # background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\staffbg.jpg")
        bg_label = Label(self.root , image=self.bg)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\staffdp.jpg")
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


        etype = Label(frame, text="Type", font=("calibri", 15, "bold"), bg="white")
        etype.place(x=370, y=170)
        self.etype_entry = ttk.Combobox(frame, textvariable=self.var_type, font=("calibri", 15), state="readonly")
        self.etype_entry["values"] = ("Select", "Nurse", "Compounder", "Cleaner","Driver","Wardboy")
        self.etype_entry.place(x=370, y=200, width=250)
        self.etype_entry.current(0)


        #third row
        contact = Label(frame, text="Contact", font=("calibri", 15, "bold"), bg="white")
        contact.place(x=50, y=240)
        self.contact_entry = ttk.Entry(frame, textvariable=self.var_contact, font=("calibri", 15))
        self.contact_entry.place(x=50, y=270, width=250)

        staffage = Label(frame, text="Age", font=("calibri", 15, "bold"), bg="white")
        staffage.place(x=370, y=240)
        self.staffage_entry = ttk.Entry(frame,textvariable = self.var_age, font=("calibri", 15))
        self.staffage_entry.place(x=370, y=270, width=250)


        #fourth row
        admitdate = Label(frame, text="Joining date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        admitdate.place(x=50, y=310)
        self.admitdate_entry = ttk.Entry(frame,textvariable = self.var_joiningdate, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=340, width=250)


        email = Label(frame, text="email ", font=("calibri", 15, "bold"), bg="white")
        email.place(x=370, y=310)
        self.email_entry = ttk.Entry(frame, textvariable=self.var_email, font=("calibri", 15))
        self.email_entry.place(x=370, y=340, width=250)


        # fifth row
        address = Label(frame, text="Address ", font=("calibri", 15, "bold"), bg="white")
        address.place(x=50, y=380)
        self.admitdate_entry = ttk.Entry(frame, textvariable=self.var_address, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=410, width=250)

        salary = Label(frame, text="Salary ", font=("calibri", 15, "bold"), bg="white")
        salary.place(x=370, y=380)
        self.salary_entry = ttk.Entry(frame, textvariable=self.var_salary, font=("calibri", 15))
        self.salary_entry.place(x=370, y=410, width=250)


        #row 6

        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\21535001\images\submit.jpg")
        img = img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame ,image=self.photoimage , command = self.registerdata , borderwidth=0 , cursor="hand2")
        b1.place(x=370,y=480,width=200)


        ########### function declaration

    def registerdata(self):
        if self.var_firstname.get()== "" or self.var_email.get()=="" or self.var_salary.get()=="" or self.var_lastname.get()=="" or self.var_gender.get()=="Select"  or self.var_address.get()=="" or  self.var_joiningdate.get()==""  or  self.var_age.get()=="" or self.var_contact.get()=="" :
            messagebox.showerror("Error" , "Please fill all the fields")

        else :
            conn = mysql.connector.connect(host="localhost",user="root",password="0000",database="hms")
            my_cur = conn.cursor()
            my_cur.execute("insert into staff (firstname,lastname,gender,type,contact,address,joiningdate,age,salary,email) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.var_firstname.get(),
                            self.var_lastname.get() ,
                            self.var_gender.get(),
                            self.var_type.get(),
                            int(self.var_contact.get()) ,
                            self.var_address.get() ,
                            self.var_joiningdate.get(),
                            int(self.var_age.get()),
                            int(self.var_salary.get()),
                            self.var_email.get())
                           )

            conn.commit()
            conn.close()
            messagebox.showinfo("Success" , "Registered Succesfully")



class Patient:
    def __init__(self,root):
        self.root = root
        self.root.title("Patient Menu")
        self.root.geometry('1500x790+0+0')

        # variables
        self.var_countinfo = StringVar()
        self.var_firstname = StringVar()
        self.var_lastname = StringVar()
        self.var_gender = StringVar()
        self.var_blood = StringVar()
        self.var_admitdate = StringVar()
        self.var_dischargedate = StringVar()
        self.var_contact = StringVar()
        self.var_status = StringVar()
        self.var_symptoms = StringVar()
        #self.var_department = StringVar()
        self.var_address = StringVar()
        self.var_fromdate = StringVar()
        self.var_tilldate = StringVar()
        self.var_searchbydrop = StringVar()
        self.var_searchbydropentry = StringVar()
        self.var_patientage = StringVar()
        self.var_patientemail = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\patientbg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4 ,bg="white" , relief = RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450 )

        scroll_x = ttk.Scrollbar(rowframe,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.patienttable=ttk.Treeview(rowframe , column=("PID" , "First name","Last name","Gender" ,"Age","Blood Type" , "Contact No" ,"Email" ,"Address" , "Admit on" , "Discharge on" , "Status" ,"Symptom" ),xscrollcommand=scroll_x.set , yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM ,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.patienttable.xview)
        scroll_y.config(command=self.patienttable.yview)

        self.patienttable.heading("PID",text="PID")
        self.patienttable.heading("First name", text="First name")
        self.patienttable.heading("Last name", text="Last name")
        self.patienttable.heading("Gender", text="Gender")
        self.patienttable.heading("Age", text="Age")
        self.patienttable.heading("Blood Type", text="Blood Type")
        self.patienttable.heading("Contact No", text="Contact No")
        self.patienttable.heading("Email", text="Email")
        self.patienttable.heading("Address", text="Address")
        self.patienttable.heading("Admit on", text="Admit on")
        self.patienttable.heading("Discharge on", text="Discharge on")
        self.patienttable.heading("Status", text="Status")
        self.patienttable.heading("Symptom", text="Symptom")
        #self.patienttable.heading("Department", text="Department")

        self.patienttable["show"]="headings"
        self.patienttable.column("PID",width=100)
        self.patienttable.column("First name", width=100)
        self.patienttable.column("Last name", width=100)
        self.patienttable.column("Gender", width=100)
        self.patienttable.column("Age", width=100)
        self.patienttable.column("Blood Type", width=100)
        self.patienttable.column("Contact No", width=100)
        self.patienttable.column("Email", width=200)
        self.patienttable.column("Address", width=200)
        self.patienttable.column("Admit on", width=100)
        self.patienttable.column("Discharge on", width=100)
        self.patienttable.column("Status", width=100)
        self.patienttable.column("Symptom", width=200)
        #self.patienttable.column("Department", width=100)

        self.patienttable.pack(fill=BOTH,expand=1)
        self.fetch_entries()


        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        registerpat = Button(topframe,command=self.patient_register_window, text="Register New Patient", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                               fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        registerpat.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe,command = self.update_patient_window, text="Update Patient Details", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.discharge_patient_window ,  text="Discharge Patient", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        dischargepat.place(x=480, y=10, width=200, height=50)




        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Patients:", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        #count info

        countinfo =  Label(navframe, text="Count", font=("calibri", 15, "bold"), bg="white")
        countinfo.place(x=500, y=10)
        self.countinfo_entry = ttk.Entry(navframe, textvariable=self.var_countinfo, font=("calibri", 15))
        self.countinfo_entry.place(x=560, y=10, width=100)


        searchby = Label(navframe, text="Search By", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=950, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable = self.var_searchbydrop , font=("calibri", 15), state="readonly")
        self.searchbydrop["values"] = ("Select", "pid", "firstname", "lastname", "gender", "age", "blood", "contact","email" , "admitdate", "dischargedate" ,"status" )
        self.searchbydrop.place(x=1050, y=10, width=100)
        self.searchbydrop.current(0)


        self.searchbar_entry = ttk.Entry(navframe,  textvariable = self.var_searchbydropentry , font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command = self.searchbyfunction ,  text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                            fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        nsearchbtn.place(x=1290, y=5, width=100)


        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        fromdate = Label(botframe, text="From date", font=("calibri", 15, "bold"), bg="white")
        fromdate.place(x=5, y=10)
        self.fromdate_entry = ttk.Entry(botframe, textvariable = self.var_fromdate, font=("calibri", 15))
        self.fromdate_entry.place(x=100, y=10, width=100)

        tilldate = Label(botframe, text="Till date", font=("calibri", 15, "bold"), bg="white")
        tilldate.place(x=210, y=10)
        self.tilldate_entry = ttk.Entry(botframe, textvariable = self.var_tilldate ,font=("calibri", 15))
        self.tilldate_entry.place(x=290, y=10, width=100)

        bsearchbtn = Button(botframe, command = self.daterangeshow ,   text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                          fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        bsearchbtn.place(x=410, y=5, width=100 ,height=40)

        showallbutton = Button(botframe, command= self.fetch_entries ,  text="Show All", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                          fg="white", bg="#1a75ff", activeforeground="white", activebackground="#1a75ff")
        showallbutton.place(x=1250, y=5, width=120, height=35)


    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from patient")
        data=my_cur.fetchall()
        if len(data)!=0:
            self.patienttable.delete(*self.patienttable.get_children())
            count=0
            for i in data:
                count = count + 1
                self.patienttable.insert("",END,values=i)
                self.var_countinfo.set(count)
                conn.commit()
            conn.close()



    def update_patient_window(self) :
                self.root2=Toplevel()
                self.root2.title("Update Patient Details")
                self.root2.geometry("600x750+500+10")

                # background image
                self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\patientbg1.jpg")
                bg_label = Label(self.root2, image=self.bg1)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                #declare variables
                self.var_firstname_update = StringVar()
                self.var_lastname_update = StringVar()
                self.var_pid_update = StringVar()
                self.var_contact_update = StringVar()
                self.var_symptoms_update = StringVar()
                self.var_address_update = StringVar()
                #self.var_department_update = StringVar()
                self.var_patientage_update = StringVar()
                self.var_patientemail_update = StringVar()

                pid_update = Label(self.root2, text="PID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                pid_update.place(x=150, y=50)
                self.pid_update_entry = ttk.Entry(self.root2, textvariable=self.var_pid_update, font=("calibri", 15))
                self.pid_update_entry.place(x=150, y=80, width=250)

                firstname_update = Label(self.root2, text="First Name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                firstname_update.place(x=150, y=120)
                self.firstname_update_entry = ttk.Entry(self.root2,textvariable = self.var_firstname_update, font=("calibri", 15))
                self.firstname_update_entry.place(x=150, y=150, width=250)

                lastname_update = Label(self.root2, text="Last name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                lastname_update.place(x=150, y=190)
                self.lastname_update_entry = ttk.Entry(self.root2, textvariable = self.var_lastname_update, font=("calibri", 15))
                self.lastname_update_entry.place(x=150, y=220, width=250)


                patientage_update = Label(self.root2, text="Age ", font=("calibri", 15, "bold"), bg="white", fg="black")
                patientage_update.place(x=150, y=260)
                self.patientage_update_entry = ttk.Entry(self.root2, textvariable=self.var_patientage_update,
                                                  font=("calibri", 15))
                self.patientage_update_entry.place(x=150, y=290, width=250)


                symptoms_update = Label(self.root2, text="Enter symptoms", font=("calibri", 15, "bold"), bg="white", fg="black")
                symptoms_update.place(x=150, y=330)
                self.symptoms_update_entry = ttk.Entry(self.root2,textvariable = self.var_symptoms_update, font=("calibri", 15))
                self.symptoms_update_entry.place(x=150, y=360, width=250)


                address_update = Label(self.root2, text="Enter Address", font=("calibri", 15, "bold"), bg="white",
                                        fg="black")
                address_update.place(x=150, y=400)
                self.address_update_entry = ttk.Entry(self.root2,textvariable = self.var_address_update, font=("calibri", 15))
                self.address_update_entry.place(x=150, y=430, width=250)



                email_update = Label(self.root2, text="Email", font=("calibri", 15, "bold"), bg="white",
                                     fg="black")
                email_update.place(x=150, y=470)
                self.contact_update_entry = ttk.Entry(self.root2, textvariable=self.var_patientemail_update,
                                                      font=("calibri", 15))
                self.contact_update_entry.place(x=150, y=500, width=250)


                contact_update = Label(self.root2, text="Enter contact no", font=("calibri", 15, "bold"), bg="white" ,fg="black")
                contact_update.place(x=150, y=540)
                self.contact_update_entry = ttk.Entry(self.root2,textvariable = self.var_contact_update, font=("calibri", 15))
                self.contact_update_entry.place(x=150, y=570, width=250)


                btn=Button(self.root2, text="Update" , command = self.update_patient,font=("calibri", 15,"bold") , fg="white",bg="#1a75ff")
                btn.place(x=150,y=610)



    def daterangeshow(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        query1= "select * from patient where (dischargedate >= %s and dischargedate <= %s) or (admitdate >= %s and admitdate <= %s)"
        value1=(self.var_fromdate.get() ,self.var_tilldate.get(),self.var_fromdate.get() ,self.var_tilldate.get())
        my_cur.execute(query1 , value1)
        data = my_cur.fetchall()
        if len(data) != 0:
            self.patienttable.delete(*self.patienttable.get_children())
            count=0
            for i in data:
                count = count + 1
                self.patienttable.insert("", END, values=i)
                self.var_countinfo.set(count)
                conn.commit()
            conn.close()


    def update_patient(self):
        #do update here
        if self.var_pid_update.get() == "" or self.var_firstname_update.get() == "" or self.var_lastname_update.get() == "" or self.var_address_update.get() == "" or self.var_contact_update.get()=="" or self.var_symptoms_update.get() == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from patient where pid=%s "
            value = (self.var_pid_update.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct patient ID", parent=self.root2)
            else :
                query = "update patient set firstname=%s,lastname=%s,contact=%s,address=%s,symptom=%s , age=%s where pid=%s"
                value = (self.var_firstname_update.get() ,
                         self.var_lastname_update.get() ,
                         int(self.var_contact_update.get()) ,
                         self.var_address_update.get() ,
                         self.var_symptoms_update.get() ,
                         self.var_patientage_update.get(),
                         self.var_pid_update.get())

                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Patient data updated " , parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()


    def discharge_patient_window(self) :
                self.root3=Toplevel()
                self.root3.title("Discharge Patient")
                self.root3.geometry("600x300+500+25")

                # background image
                self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\patientbg.jpg")
                bg_label = Label(self.root3, image=self.bg1)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                #declare variables
                self.var_dischargedate_discharge = StringVar()
                self.var_pid_discharge = StringVar()

                pid_discharge = Label(self.root3, text="Enter PID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                pid_discharge.place(x=150, y=40)
                self.pid_discharge_entry = ttk.Entry(self.root3, textvariable=self.var_pid_discharge, font=("calibri", 15))
                self.pid_discharge_entry.place(x=150, y=70, width=250)

                dischargedate_discharge = Label(self.root3, text="Enter Discharge date ", font=("calibri", 15, "bold"), bg="white", fg="black")
                dischargedate_discharge.place(x=150, y=110)
                self.dischargedate_discharge_entry = ttk.Entry(self.root3,textvariable = self.var_dischargedate_discharge, font=("calibri", 15))
                self.dischargedate_discharge_entry.place(x=150, y=140, width=250)

                btn_discharge=Button(self.root3, text="Discharge" , command = self.discharge_patient,font=("calibri", 15,"bold") , fg="white",bg="#1a75ff")
                btn_discharge.place(x=150,y=180)


    def discharge_patient(self):
        if self.var_pid_discharge.get() == ""  or self.dischargedate_discharge_entry.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from patient where pid=%s "
            value = (self.var_pid_discharge.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct patient ID", parent=self.root3)
            else :
                query = "update patient set status='Discharged',dischargedate=%s where pid=%s"
                value = (self.dischargedate_discharge_entry.get() ,
                         self.var_pid_discharge.get())


                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Patient discharged " , parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()




    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select"  or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                self.patienttable.delete(*self.patienttable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select * from patient where " + str(self.var_searchbydrop.get()) + " = '" + str(self.var_searchbydropentry.get())+ "'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.patienttable.delete(*self.patienttable.get_children())
                    count=0
                    for i in data1:
                        count = count + 1
                        self.patienttable.insert("", END, values=i)
                        self.var_countinfo.set(count)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error" , f"Due To:{str(es)}",parent=self.root)

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
        #self.var_dischargedate = StringVar()
        self.var_contact = StringVar()
        self.var_status = StringVar()
        self.var_symptoms = StringVar()
        self.var_department = StringVar()
        self.var_address = StringVar()
        self.var_age = StringVar()
        self.var_email = StringVar()


        # background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\patientbg.jpg")
        bg_label = Label(self.root , image=self.bg)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\pat.jpg")
        bg1_label = Label(self.root, image=self.bg1)
        bg1_label.place(x=50, y=100, width=470, height=600)

        #main frame
        frame = Frame(self.root , bg="white")
        frame.place(x=520,y=100,width=800,height=600)

        #register here text
        register_lbl = Label(frame , text="Register here" , font=("calibri",25,"bold"),fg="green",bg="white")
        register_lbl.place(x=30,y=20)

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

        patientage = Label(frame, text="Age", font=("calibri", 15, "bold"), bg="white")
        patientage.place(x=370, y=240)
        self.patientage_entry = ttk.Entry(frame,textvariable = self.var_age, font=("calibri", 15))
        self.patientage_entry.place(x=370, y=270, width=250)


        #fourth row
        admitdate = Label(frame, text="Admit date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        admitdate.place(x=50, y=310)
        self.admitdate_entry = ttk.Entry(frame,textvariable = self.var_admitdate, font=("calibri", 15))
        self.admitdate_entry.place(x=50, y=340, width=250)

        email = Label(frame, text="Email", font=("calibri", 15, "bold"), bg="white")
        email.place(x=370, y=310)
        self.email_entry = ttk.Entry(frame, textvariable=self.var_email, font=("calibri", 15))
        self.email_entry.place(x=370, y=340, width=250)




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

        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\21535001\images\submit.jpg")
        img = img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame ,image=self.photoimage , command = self.registerdata , borderwidth=0 , cursor="hand2")
        b1.place(x=370,y=480,width=200)


        ########### function declaration

    def registerdata(self):
        if self.var_firstname.get()=="" or self.var_lastname.get()=="" or self.var_address.get()=="" or self.var_symptoms.get()=="" or self.var_admitdate=="" or self.var_gender.get()=="Select" or self.var_blood.get()=="Select" or self.var_age.get()==""  :
            messagebox.showerror("Error" , "Please fill all the fields")

        else :
            conn = mysql.connector.connect(host="localhost",user="root",password="0000",database="hms")
            my_cur = conn.cursor()
            my_cur.execute("insert into patient (firstname,lastname,gender,blood,contact,email,address,admitdate,age,symptom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.var_firstname.get(),
                            self.var_lastname.get() ,
                            self.var_gender.get(),
                            self.var_blood.get(),
                            int(self.var_contact.get()) ,
                            self.var_email.get() ,
                            self.var_address.get() ,
                            self.var_admitdate.get(),
                            int(self.var_age.get()),
                            self.var_symptoms.get(),
                            ))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success" , "Registered Succesfully")



class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Admin Registration")
        self.root.geometry('1600x800+0+0')

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
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\adminregisterbg.jpg")
        bg_label = Label(self.root , image=self.bg)
        bg_label.place(x=0,y=0,relwidth=1,relheight=1)

        # side image
        self.bg1 = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\21535001\images\adminregister.jpg")
        bg1_label = Label(self.root, image=self.bg1)
        bg1_label.place(x=100, y=100, width=470, height=550)

        #main frame
        frame = Frame(self.root , bg="white")
        frame.place(x=570,y=100,width=800,height=550)

        #register here text
        register_lbl = Label(frame , text="Admin Registration" , font=("calibri",25,"bold"),fg="purple",bg="white")
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

        email = Label(frame, text="Enter username", font=("calibri", 15, "bold"), bg="white")
        email.place(x=370, y=170)

        self.email_entry = ttk.Entry(frame,textvariable = self.var_email, font=("calibri", 15))
        self.email_entry.place(x=370, y=200, width=250)

        #third row
        SecurityQ = Label(frame, text="Choose Security Question", font=("calibri", 15, "bold"), bg="white")
        SecurityQ.place(x=50, y=240)

        self.SecurityQ_entry = ttk.Combobox(frame,textvariable = self.var_SecurityQ, font=("calibri", 15),state="readonly")
        self.SecurityQ_entry["values"] = ("Select", "Enter birth place", "Enter petname", "Enter bestfriend name")
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
        chkbox = Checkbutton(frame ,variable = self.var_chkbox, text="I agree to all terms and conditions" , font=("calibri", 15, "bold") , onvalue=1,offvalue=0)
        chkbox.place(x=50,y=390)

        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\21535001\images\submit.jpg")
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
            query = ("select * from admin where email=%s")
            value=(self.var_email.get(),)
            my_cur.execute(query,value)
            row = my_cur.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist/registered")
            else:
                my_cur.execute("insert into admin (fname ,lname,contact,email,SecurityQ , SecurityA ,passwd) values(%s,%s,%s,%s,%s,%s,%s)",(self.var_fname.get(),self.var_lname.get() ,int(self.var_contact.get()), self.var_email.get(),self.var_SecurityQ.get() , self.var_SecurityA.get() , self.var_passwd.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success" , "Registered Succesfully")


if __name__ == "__main__":
    main()