from tkinter import*
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import mysql.connector

def main():
    win = Tk()
    app = Doctor(win)
    win.mainloop()


class Doctor:
    def __init__(self,root):
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
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4 ,bg="white" , relief = RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450 )

        scroll_x = ttk.Scrollbar(rowframe,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.doctortable=ttk.Treeview(rowframe , column=("DID" , "First name","Last name", "Age" ,"Gender" , "Contact No" ,"Email" ,"Address" , "Qualification" , "Department" ,"Salary"  , "Status" ,"Cabin" ,"Joining date" , "Resign date"),xscrollcommand=scroll_x.set , yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM ,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.doctortable.xview)
        scroll_y.config(command=self.doctortable.yview)

        self.doctortable.heading("DID",text="DID")
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


        self.doctortable["show"]="headings"
        self.doctortable.column("DID",width=100)
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

        self.doctortable.pack(fill=BOTH,expand=1)
        self.fetch_entries()


        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)

        registerdoctor = Button(topframe,command=self.doctor_register_window, text="Register doctor", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                               fg="white", bg="blue", activeforeground="white", activebackground="blue")
        registerdoctor.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe,command = self.update_doctor_window, text="Update doctor Details", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.discharge_doctor_window ,  text="Dismiss doctor", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
        dischargepat.place(x=480, y=10, width=200, height=50)

        appointmentbyid = Button(topframe, command=self.appointmentby_id, text="Appointment by ID",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="blue", activeforeground="white", activebackground="blue")
        appointmentbyid.place(x=710, y=10, width=200, height=50)


        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="doctor :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=950, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable = self.var_searchbydrop , font=("calibri", 15), state="readonly")
        self.searchbydrop["values"] = ("Select", "did", "firstname", "lastname", "gender", "age",  "contact", "email", "address" ,"qualification" ,"status" , "department","salary" , "cabin" ,"joiningdate","resigndate")
        self.searchbydrop.place(x=1050, y=10, width=100)
        self.searchbydrop.current(0)


        self.searchbar_entry = ttk.Entry(navframe,  textvariable = self.var_searchbydropentry , font=("calibri", 15))
        self.searchbar_entry.place(x=1170, y=10, width=100)

        nsearchbtn = Button(navframe, command = self.searchbyfunction ,  text="Search", font=("calibri", 15, "bold"), bd=2, relief=RIDGE,
                            fg="white", bg="blue", activeforeground="white", activebackground="blue")
        nsearchbtn.place(x=1290, y=5, width=100)


        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)


        showallbutton = Button(botframe, command= self.fetch_entries ,  text="Show All", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                          fg="white", bg="blue", activeforeground="white", activebackground="blue")
        showallbutton.place(x=1250, y=5, width=120, height=35)


    def fetch_entries(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
        my_cur = conn.cursor()
        my_cur.execute("select * from doctor")
        data=my_cur.fetchall()
        if len(data)!=0:
            self.doctortable.delete(*self.doctortable.get_children())
            for i in data:
                self.doctortable.insert("",END,values=i)
                conn.commit()
            conn.close()

    def appointmentby_id(self):
        self.root6 = Toplevel()
        self.root6.title("Appointment by DID")
        self.root6.geometry('1100x500+250+100')

        # variables
        self.var_did = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root6, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root6, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=110, width=1000, height=350)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe, column=(
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
        navframe = Frame(self.root6, bg="white")
        navframe.place(x=50, y=50, width=1000, height=50)

        searchby = Label(navframe, text="Enter Doctor ID :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=5, y=10)
        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_did, font=("calibri", 15))
        self.searchbar_entry.place(x=170, y=10, width=100)

        nsearchbtn = Button(navframe, command=self.searchbyfunctionaid, text="Search", font=("calibri", 15, "bold"),
                            bd=2,
                            relief=RIDGE,
                            fg="white", bg="blue", activeforeground="white", activebackground="blue")
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


    def update_doctor_window(self) :
                self.root2=Toplevel()
                self.root2.title("Update doctor Details")
                self.root2.geometry("850x550+400+50")

                #declare variables
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



                did_update = Label(self.root2, text="Enter valid DID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                did_update.place(x=150, y=80)
                self.did_update_entry = ttk.Entry(self.root2, textvariable=self.var_did_update, font=("calibri", 15))
                self.did_update_entry.place(x=150, y=110, width=250)

                firstname_update = Label(self.root2, text="First Name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                firstname_update.place(x=450, y=80)  #150
                self.firstname_update_entry = ttk.Entry(self.root2,textvariable = self.var_firstname_update, font=("calibri", 15))
                self.firstname_update_entry.place(x=450, y=110, width=250) #180


                doctorage_update = Label(self.root2, text="Age ", font=("calibri", 15, "bold"), bg="white", fg="black")
                doctorage_update.place(x=150, y=150)
                self.doctorage_update_entry = ttk.Entry(self.root2, textvariable=self.var_doctorage_update,
                                                        font=("calibri", 15))
                self.doctorage_update_entry.place(x=150, y=180, width=250)

                lastname_update = Label(self.root2, text="Last name ", font=("calibri", 15, "bold"), bg="white", fg="black")
                lastname_update.place(x=450, y=150)
                self.lastname_update_entry = ttk.Entry(self.root2, textvariable = self.var_lastname_update, font=("calibri", 15))
                self.lastname_update_entry.place(x=450, y=180, width=250)


                salary_update = Label(self.root2, text="Enter salary", font=("calibri", 15, "bold"), bg="white", fg="black")
                salary_update.place(x=150, y=220)
                self.salary_update_entry = ttk.Entry(self.root2,textvariable = self.var_salary_update, font=("calibri", 15))
                self.salary_update_entry.place(x=150, y=250, width=250)

                address_update = Label(self.root2, text="Enter Address", font=("calibri", 15, "bold"), bg="white",
                                        fg="black")
                address_update.place(x=450, y=220)
                self.address_update_entry = ttk.Entry(self.root2,textvariable = self.var_address_update, font=("calibri", 15))
                self.address_update_entry.place(x=450, y=250, width=250)


                email_update = Label(self.root2, text="Enter email", font=("calibri", 15, "bold"), bg="white",
                                       fg="black")
                email_update.place(x=150, y=290)
                self.email_update_entry = ttk.Entry(self.root2, textvariable=self.var_email_update,
                                                      font=("calibri", 15))
                self.email_update_entry.place(x=150, y=320, width=250)

                contact_update = Label(self.root2, text="Enter contact no", font=("calibri", 15, "bold"), bg="white" ,fg="black")
                contact_update.place(x=450, y=290)
                self.contact_update_entry = ttk.Entry(self.root2,textvariable = self.var_contact_update, font=("calibri", 15))
                self.contact_update_entry.place(x=450, y=320, width=250)


                qualification_update = Label(self.root2, text="Enter Qualification", font=("calibri", 15, "bold"), bg="white",
                                     fg="black")
                qualification_update.place(x=150, y=360)
                self.qualification_update_entry = ttk.Combobox(self.root2, textvariable=self.var_qualification_update,
                                                    font=("calibri", 15) , state="readonly")
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

                btn=Button(self.root2, text="Update" , command = self.update_doctor,font=("calibri", 15,"bold") , fg="white",bg="blue")
                btn.place(x=370,y=450 , width = 100)



    def update_doctor(self):
        #do update here
        if self.var_did_update.get() == "" or self.var_doctorage_update.get() == "" or self.var_firstname_update.get() == "" or self.var_lastname_update.get() == "" or self.var_address_update.get() == "" or self.var_contact_update.get()=="" or self.var_email_update.get() == "" or self.var_qualification_update.get()=="Select"  or self.var_salary_update.get() == "" or self.var_cabin_update.get()=="" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from doctor where did=%s "
            value = (self.var_did_update.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct doctor ID", parent=self.root2)
            else :
                query = "update doctor set firstname=%s,lastname=%s,contact=%s,address=%s,email=%s,salary=%s , age=%s , qualification=%s , cabin=%s where did=%s"
                value = (self.var_firstname_update.get() ,
                         self.var_lastname_update.get() ,
                         int(self.var_contact_update.get()) ,
                         self.var_address_update.get() ,
                         self.var_email_update.get() ,
                         int(self.var_salary_update.get()),
                         self.var_doctorage_update.get(),
                         self.var_qualification_update.get(),
                         self.var_cabin_update.get(),
                         self.var_did_update.get())

                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "doctor data updated " , parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()

    def discharge_doctor_window(self) :
                self.root3=Toplevel()
                self.root3.title("Remove doctor")
                self.root3.geometry("600x300+500+25")

                #declare variables
                self.var_resigndate = StringVar()
                self.var_did_resign = StringVar()

                pid_resign = Label(self.root3, text="DID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                pid_resign.place(x=150, y=40)
                self.pid_resign_entry = ttk.Entry(self.root3, textvariable=self.var_did_resign, font=("calibri", 15))
                self.pid_resign_entry.place(x=150, y=70, width=250)

                resigndate= Label(self.root3, text="Enter Resign date ", font=("calibri", 15, "bold"), bg="white", fg="black")
                resigndate.place(x=150, y=110)
                self.resigndate_entry = ttk.Entry(self.root3,textvariable = self.var_resigndate ,font=("calibri", 15))
                self.resigndate_entry.place(x=150, y=140, width=250)

                btn_discharge=Button(self.root3, text="Submit " , command = self.discharge_doctor,font=("calibri", 15,"bold") , fg="white",bg="blue")
                btn_discharge.place(x=150,y=180)

    def discharge_doctor(self):
        if self.var_did_resign.get() == ""  or self.var_resigndate.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from doctor where did=%s "
            value = (self.var_did_resign.get(),)
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter the correct doctor ID", parent=self.root3)
            else :
                query = "update doctor set status='resigned',resigndate=%s where did=%s"
                value = (self.var_resigndate.get() ,
                         self.var_did_resign.get())


                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "doctor removed " , parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select"  or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select * from doctor where " + str(self.var_searchbydrop.get()) + " LIKE '%" + str(self.var_searchbydropentry.get())+ "%'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.doctortable.delete(*self.doctortable.get_children())
                    for i in data1:
                        self.doctortable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error" , f"Due To:{str(es)}",parent=self.root)

    def doctor_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = doctor_Register(self.new_window)



class doctor_Register:
    def __init__(self,root):
        self.root = root
        self.root.title("doctor Registration")
        self.root.geometry('1600x900+0+0')

        #variables
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


        qualification = Label(frame, text="Qualification", font=("calibri", 15, "bold"), bg="white")
        qualification.place(x=370, y=170)
        self.qualification_entry = ttk.Combobox(frame, textvariable=self.var_qualification, font=("calibri", 15), state="readonly")
        self.qualification_entry["values"] = ("Select", "MBBS", "MD", "MCH","BDS","BHMS" , "BAMS")
        self.qualification_entry.place(x=370, y=200, width=250)
        self.qualification_entry.current(0)


        #third row
        contact = Label(frame, text="Contact", font=("calibri", 15, "bold"), bg="white")
        contact.place(x=50, y=240)
        self.contact_entry = ttk.Entry(frame, textvariable=self.var_contact, font=("calibri", 15))
        self.contact_entry.place(x=50, y=270, width=250)

        doctorage = Label(frame, text="Age", font=("calibri", 15, "bold"), bg="white")
        doctorage.place(x=370, y=240)
        self.doctorage_entry = ttk.Entry(frame,textvariable = self.var_doctorage, font=("calibri", 15))
        self.doctorage_entry.place(x=370, y=270, width=250)


        #fourth row
        admitdate = Label(frame, text="Joining date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white")
        admitdate.place(x=50, y=310)
        self.admitdate_entry = ttk.Entry(frame,textvariable = self.var_joiningdate, font=("calibri", 15))
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


        #row 6
        department = Label(frame, text="Department ", font=("calibri", 15, "bold"), bg="white")
        department.place(x=50, y=450)
        self.department_entry = ttk.Combobox(frame, textvariable=self.var_department, font=("calibri", 15),state="readonly")
        self.department_entry["values"] = ("Select", "General", "Gynaechology","Dental","Cardiology","Neurology","Dermatology","Radiology","Surgical")
        self.department_entry.place(x=50, y=480, width=250)
        self.department_entry.current(0)


        cabin = Label(frame, text="Cabin no", font=("calibri", 15, "bold"), bg="white")
        cabin.place(x=370, y=450)
        self.cabin_entry = ttk.Entry(frame, textvariable=self.var_cabin, font=("calibri", 15))
        self.cabin_entry.place(x=370, y=480, width=250)


        #row7
        #buttons part
        img = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\submit.jpg")
        img = img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame ,image=self.photoimage , command = self.registerdata , borderwidth=0 , cursor="hand2")
        b1.place(x=250,y=530,width=200)


        ########### function declaration

    def registerdata(self):
        if self.var_firstname.get()== "" or self.var_cabin =="" or self.var_department == "Select" or self.var_qualification.get()=="Select" or self.var_doctoremail.get()=="" or self.var_salary.get()=="" or self.var_lastname.get()=="" or self.var_gender.get()=="Select"  or self.var_address.get()=="" or  self.var_joiningdate.get()==""  or  self.var_doctorage.get()=="" or self.var_contact.get()=="" :
            messagebox.showerror("Error" , "Please fill all the fields")

        else :
            conn = mysql.connector.connect(host="localhost",user="root",password="0000",database="hms")
            my_cur = conn.cursor()
            my_cur.execute("insert into doctor (firstname,lastname,gender,qualification,contact,address,joiningdate,age,salary,email,department,cabin) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.var_firstname.get(),
                            self.var_lastname.get() ,
                            self.var_gender.get(),
                            self.var_qualification.get(),
                            int(self.var_contact.get()) ,
                            self.var_address.get() ,
                            self.var_joiningdate.get(),
                            int(self.var_doctorage.get()),
                            int(self.var_salary.get()),
                            self.var_doctoremail.get(),
                            self.var_department.get(),
                            self.var_cabin.get())
                           )

            conn.commit()
            conn.close()
            messagebox.showinfo("Success" , "Registered Succesfully")







if __name__ == "__main__" :
    main()