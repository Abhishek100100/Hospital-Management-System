from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector


def main():
    win = Tk()
    app = Emergency(win)
    win.mainloop()


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
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
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
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.reschedule_duty_window, text="Reschedule duty",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="blue", activeforeground="white", activebackground="blue")
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
                            fg="white", bg="blue", activeforeground="white", activebackground="blue")
        nsearchbtn.place(x=1290, y=5, width=100)

        # bottom frame
        botframe = Frame(self.root, bg="white")
        botframe.place(x=50, y=650, width=1400, height=50)

        showallbutton = Button(botframe, command=self.fetch_entries, text="Show All", font=("calibri", 15, "bold"),
                               bd=3, relief=RIDGE,
                               fg="white", bg="blue", activeforeground="white", activebackground="blue")
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
                     bg="blue")
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
                               font=("calibri", 15, "bold"), fg="white", bg="blue")
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


if __name__ == "__main__":
    main()