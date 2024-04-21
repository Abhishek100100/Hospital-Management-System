from tkinter import*
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import mysql.connector

def main():
    win = Tk()
    app = Staff(win)
    win.mainloop()


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
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
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
                               fg="white", bg="blue", activeforeground="white", activebackground="blue")
        registerstaff.place(x=20, y=10, width=200, height=50)

        updatepat = Button(topframe,command = self.update_staff_window, text="Update staff Details", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=250, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.discharge_staff_window ,  text="Dismiss staff", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
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

                btn=Button(self.root2, text="Update" , command = self.update_staff,font=("calibri", 15,"bold") , fg="white",bg="blue")
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

                btn_discharge=Button(self.root3, text="Submit " , command = self.discharge_staff,font=("calibri", 15,"bold") , fg="white",bg="blue")
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
        img = Image.open(r"C:\Users\abhib\Desktop\GUIproject\images\submit.jpg")
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







if __name__ == "__main__" :
    main()