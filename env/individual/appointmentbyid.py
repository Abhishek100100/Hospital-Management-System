from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector


def main():
    win = Tk()
    app = Appointmentbydid(win)
    win.mainloop()

class Appointmentbydid:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment by DID")
        self.root.geometry('1100x500+250+100')

        # variables
        self.var_did = StringVar()

        # background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # main frame for table
        rowframe = Frame(self.root, bd=4, bg="white", relief=RIDGE)
        rowframe.place(x=50, y=110, width=1000, height=350)

        scroll_x = ttk.Scrollbar(rowframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(rowframe, orient=VERTICAL)
        self.appointtable = ttk.Treeview(rowframe, column=(
        "Doctor ID","Appointment Status" ,"Date","Time" ,"Patient firstname", "Patient lastname", "Patient gender",
         "Patient bloodtype", "Admit date","Symptoms" , "Patient contact no" ,"Patient ID", "Appointment ID"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

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
        navframe = Frame(self.root, bg="white")
        navframe.place(x=50, y=50, width=1000, height=50)

        searchby = Label(navframe, text="Enter Doctor ID :", font=("calibri", 15, "bold"), bg="white")
        searchby.place(x=5, y=10)
        self.searchbar_entry = ttk.Entry(navframe, textvariable=self.var_did, font=("calibri", 15))
        self.searchbar_entry.place(x=170, y=10, width=100)


        nsearchbtn = Button(navframe, command=self.searchbyfunctionaid, text="Search", font=("calibri", 15, "bold"), bd=2,
                            relief=RIDGE,
                            fg="white", bg="blue", activeforeground="white", activebackground="blue")
        nsearchbtn.place(x=290, y=10, width=100 , height=30)






    def searchbyfunctionaid(self):
        if self.var_did.get() == "" :
            messagebox.showerror("Error", "Please fill the field")
        else:
            try:
                self.appointtable.delete(*self.appointtable.get_children())
                conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="hms")
                my_cur = conn.cursor()
                query = "select distinct doctor.did,appointment.status , appointment.dates , appointment.timing , patient.firstname ,patient.lastname,patient.gender,patient.blood,patient.admitdate,patient.symptom , patient.contact , patient.pid , appointment.aid from appointment , patient , doctor where doctor.did =%s and appointment.pid = patient.pid and appointment.did = doctor.did and doctor.status ='employee' and patient.status = 'Admitted'"
                value =  ( int(self.var_did.get()) ,)
                my_cur.execute(query,value)
                data1 = my_cur.fetchall()
                if len(data1) != 0:
                    self.appointtable.delete(*self.appointtable.get_children())
                    for i in data1:
                        self.appointtable.insert("", END, values=i)
                        conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

if __name__ == "__main__":
    main()