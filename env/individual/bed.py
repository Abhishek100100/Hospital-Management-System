from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector


def main():
    win = Tk()
    app = Bed(win)
    win.mainloop()


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
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\abhib\Desktop\GUIproject\images\bg.jpg")
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
                           fg="white", bg="blue", activeforeground="white", activebackground="blue")
        updatepat.place(x=20, y=10, width=200, height=50)

        dischargepat = Button(topframe, command=self.set_bedcost_window, text="Set Bed Cost",
                              font=("calibri", 15, "bold"), bd=3, relief=RIDGE,
                              fg="white", bg="blue", activeforeground="white", activebackground="blue")
        dischargepat.place(x=250, y=10, width=200, height=50)

        deletebed = Button(topframe, command=self.delete_bed_window, text="Delete Bed", font=("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="blue", activeforeground="white", activebackground="blue")
        deletebed.place(x=480, y=10, width=200, height=50)

        allotbed = Button(topframe, command=self.allot_bed_window, text="Allot bed",
                           font=("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="blue",
                           activeforeground="white", activebackground="blue")
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


        bedid = Label(self.root2, text="Enter Bed ID", font=("calibri", 15, "bold"), bg="white", fg="black")
        bedid.place(x=150, y=150)
        self.bedid_entry = ttk.Entry(self.root2, textvariable=self.var_bedid, font=("calibri", 15))
        self.bedid_entry.place(x=150, y=180, width=300)


        btn = Button(self.root2, text="Delete", command=self.delete_bed, font=("calibri", 15, "bold"), fg="white",
                     bg="blue")
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
                     bg="blue")
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
                               font=("calibri", 15, "bold"), fg="white", bg="blue")
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
                               font=("calibri", 15, "bold"), fg="white", bg="blue")
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


if __name__ == "__main__":
    main()