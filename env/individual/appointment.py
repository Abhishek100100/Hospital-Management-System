from tkinter import*
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import mysql.connector

def main():
    win = Tk()
    app = Appointment(win)
    win.mainloop()

class Appointment:
    def __init__(self,root):
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
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4 ,bg="white" , relief = RIDGE)
        rowframe.place(x=50, y=180, width=1400, height=450 )

        scroll_x = ttk.Scrollbar(rowframe,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable=ttk.Treeview(rowframe , column=("AppointmentID" , "Status", "Date","Time"  ,"Patient firstname" ,"Patient lastname" , "Patient contact no" ,"Doctor firstname" ,"Doctor lastname" , "Doctor contact no" ,"Cabin no" , "Department" ,"Patient ID", "Doctor ID"),xscrollcommand=scroll_x.set , yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM ,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.appointtable.xview)
        scroll_y.config(command=self.appointtable.yview)
#make channges here
        self.appointtable.heading("AppointmentID",text="AppointmentID")
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



        self.appointtable["show"]="headings"
        self.appointtable.column("AppointmentID",width=100)
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

        self.appointtable.pack(fill=BOTH,expand=1)
        self.fetch_entries()


        ######################### button frame #########################
        topframe = Frame(self.root, bg="white")
        topframe.place(x=50, y=30, width=1400, height=70)


        updatepat = Button(topframe,command = self.book_appointment_window, text="Book appointment", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                             fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.cancel_appointment_window ,  text="Cancel Appointment", font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
        dischargepat.place(x=250, y=10, width=200, height=50)



        # nav frame
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=120, width=1400, height=50)

        pattext = Label(navframe, text="Appointments :", font=("calibri", 15, "bold"), bg="white")
        pattext.place(x=5, y=10)

        searchby = Label(navframe, text="Search By :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=900, y=10)

        self.searchbydrop = ttk.Combobox(navframe, textvariable = self.var_searchbydrop , font=("calibri", 12), state="readonly")
        self.searchbydrop["values"] = ("Select", "appointment.aid","appointment.pid","appointment.did","appointment.status" , "appointment.dates" , "appointment.timing", "patient.firstname", "patient.lastname", "doctor.firstname", "doctor.lastname", "doctor.cabin", "doctor.department"  )
        self.searchbydrop.place(x=1000, y=10, width=150 , height = 30)
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
        my_cur.execute("select distinct  appointment.aid , appointment.status , appointment.dates , appointment.timing , patient.firstname , patient.lastname , patient.contact ,doctor.firstname , doctor.lastname , doctor.contact, doctor.cabin , doctor.department , appointment.pid ,appointment.did from appointment , patient , doctor where appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted'")
        data=my_cur.fetchall()
        if len(data)!=0:
            self.appointtable.delete(*self.appointtable.get_children())
            for i in data:
                self.appointtable.insert("",END,values=i)
                conn.commit()
            conn.close()


    def book_appointment_window(self) :
                self.root2=Toplevel()
                self.root2.title("Book appointment")
                self.root2.geometry("600x500+500+50")

                #declare variables

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
                self.did_entry = ttk.Entry(self.root2,textvariable = self.var_did, font=("calibri", 15))
                self.did_entry.place(x=150, y=180, width=300)

                bdate = Label(self.root2, text="Booking date(YYYY-MM-DD)", font=("calibri", 15, "bold"), bg="white", fg="black")
                bdate.place(x=150, y=220)
                self.bdate_entry = ttk.Entry(self.root2, textvariable = self.var_date, font=("calibri", 15))
                self.bdate_entry.place(x=150, y=250, width=300)


                btime = Label(self.root2, text="Booking time (HH:MM:SS)", font=("calibri", 15, "bold"), bg="white", fg="black")
                btime.place(x=150, y=290)
                self.btime_entry = ttk.Entry(self.root2, textvariable=self.var_time,
                                                  font=("calibri", 15))
                self.btime_entry.place(x=150, y=320, width=300)


                btn=Button(self.root2, text="Book" , command = self.book_appointment,font=("calibri", 15,"bold") , fg="white",bg="blue")
                btn.place(x=150,y=360)



    def book_appointment(self):
        #do update here
        if self.var_pid.get() == "" or self.var_did.get() == "" or self.var_date.get() == "" or self.var_time.get() == "" :
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()

            query = "select patient.pid , doctor.did from  patient ,doctor where patient.pid = %s and doctor.did = %s and doctor.status ='employee' and patient.status = 'Admitted'"
            value = (int(self.var_pid.get()),int(self.var_did.get()) )
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Enter valid IDs", parent=self.root2)
            else :
                query = "insert into appointment (pid,did,dates,timing) values (%s,%s,%s,%s)"
                value = (int(self.var_pid.get()) ,
                         int(self.var_did.get()) ,
                         self.var_date.get() ,
                         self.var_time.get())
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Booking Confirmed " , parent=self.root2)
                self.fetch_entries()
                self.root2.destroy()
                

    def cancel_appointment_window(self) :
                self.root3=Toplevel()
                self.root3.title("Cancel appointment")
                self.root3.geometry("600x500+500+25")

                #declare variables
                self.var_canceldate = StringVar()
                self.var_aid_cancel = StringVar()
                self.var_bookingtime = StringVar()

                pid_resign = Label(self.root3, text="Enter appointment ID ", font=("calibri", 15, "bold"), bg="white", fg="black")
                pid_resign.place(x=150, y=40)
                self.pid_resign_entry = ttk.Entry(self.root3, textvariable=self.var_aid_cancel, font=("calibri", 15))
                self.pid_resign_entry.place(x=150, y=70, width=250)

                resigndate= Label(self.root3, text="Enter booked date ", font=("calibri", 15, "bold"), bg="white", fg="black")
                resigndate.place(x=150, y=110)
                self.resigndate_entry = ttk.Entry(self.root3,textvariable = self.var_canceldate ,font=("calibri", 15))
                self.resigndate_entry.place(x=150, y=140, width=250)

                resigntime = Label(self.root3, text="Enter booked time", font=("calibri", 15, "bold"), bg="white",
                                   fg="black")
                resigntime.place(x=150, y=180)
                self.resigntime_entry = ttk.Entry(self.root3, textvariable=self.var_bookingtime, font=("calibri", 15))
                self.resigntime_entry.place(x=150, y=210, width=250)

                btn_discharge=Button(self.root3, text="Cancel " , command = self.cancel_appointment,font=("calibri", 15,"bold") , fg="white",bg="blue")
                btn_discharge.place(x=250,y=300)
        

    def cancel_appointment(self):
        if self.var_aid_cancel.get() == ""  or self.var_canceldate.get() == "" or self.var_bookingtime.get()=="":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
            my_cur = conn.cursor()
            query = "select * from appointment where aid=%s and dates=%s and timing=%s "
            value = (self.var_aid_cancel.get(),self.var_canceldate.get(),self.var_bookingtime.get())
            my_cur.execute(query, value)
            row = my_cur.fetchone()
            if row==None:
                messagebox.showerror("Error", "Please enter correct details", parent=self.root3)
            else :
                query = "update appointment set status='cancelled' where aid=%s"
                value = (self.var_aid_cancel.get() ,)
                my_cur.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Appointment cancelled " , parent=self.root3)
                self.fetch_entries()
                self.root3.destroy()

    def searchbyfunction(self):
        if self.var_searchbydrop.get() == "Select"  or self.var_searchbydropentry.get() == "":
            messagebox.showerror("Error", "Please fill the fields")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                my_cur.execute("select distinct  appointment.aid , appointment.status , appointment.dates , appointment.timing , patient.firstname , patient.lastname , patient.contact ,doctor.firstname , doctor.lastname , doctor.contact, doctor.cabin , doctor.department , appointment.pid ,appointment.did from appointment , patient , doctor where appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted' and " + str(self.var_searchbydrop.get()) + " = '" + str(self.var_searchbydropentry.get())+"'")
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error" , f"Due To:{str(es)}",parent=self.root)

    def appoint_register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = appoint_Register(self.new_window)

if __name__ == "__main__" :
    main()