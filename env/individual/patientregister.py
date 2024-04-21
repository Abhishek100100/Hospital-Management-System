from tkinter import*
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import mysql.connector

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


if __name__ == "__main__" :
    root=Tk()
    app = Patient_Register(root)
    root.mainloop()