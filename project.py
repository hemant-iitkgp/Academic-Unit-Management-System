import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re
#importing neccessary libraries and toolkits
class Address:
    def __init__(self, house, city, pincode, state):
        self.house = house
        self.city = city
        self.pincode = pincode
        self.state = state
# adresss class going to be just for aggregation with student class
class Person:
    number_of_people = 0

    def __init__(self, id, pwd, type):
        self.status = 0
        self.type = type
        self.user_id = id
        self.password = pwd
        self.name = ''
        self.dob = ''
        self.gender = -1
        self.department = ''
        self.phone = 0
        Person.number_of_people += 1

    def setPassword(self, newpwd):
        self.password = newpwd

    def changeName(self, name):
        self.name = name

    def changePhone(self, newph):
        self.phone = newph

    def changeDOB(self, newdob):
        self.dob = newdob

    def setDetails(self, name, dob, gender, department, phone):
        self.status = 1
        self.name = name
        self.dob = dob
        self.gender = gender
        self.department = department
        self.phone = phone

    def deactive(self):
        self.status = -1
# Person class is parent class/ super class for all of the following class, hance most of the necessary/common attributes are declared here
class Teacher(Person):
    number_of_teachers = 0

    def __init__(self, id, pwd, type):
        self.warden = ''
        self.post = ''
        Teacher.number_of_teachers += 1
        super().__init__(id, pwd, type)

    def changeWarden(self, warden):
        self.warden = warden

    def changePost(self, post):
        self.post = post

    def setDetails(self, name, dob, gender, department, phone, warden, post):
        self.warden = warden
        self.post = post
        super().setDetails(name, dob, gender, department, phone)

class Student(Person):
    number_of_students = 0

    def __init__(self, id, pwd, type):
        self.year_of_admission = 0
        self.cgpa = 0
        self.hall = ''
        self.address = Address(0, '', 0, '')  # Utilize the Address class
        Student.number_of_students += 1
        super().__init__(id, pwd, type)

    def setDetails(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address):
        self.year_of_admission = year_of_admission
        self.cgpa = cgpa
        self.hall = hall
        self.address = address
        super().setDetails(name, dob, gender, department, phone)

    def changeCGPA(self, newcgpa):
        self.cgpa = newcgpa

    def changeHall(self, newhall):
        self.hall = newhall

    def changeAddress(self, newadd):
        self.address = newadd

class UG(Student):
    number_of_ugs = 0

    def __init__(self, id, pwd, type):
        UG.number_of_ugs += 1
        self.EAA = ''
        super().__init__(id, pwd, type)

    def setDetails(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address, EAA):
        self.EAA = EAA
        super().setDetails(name, dob, gender, department, phone, year_of_admission, cgpa, hall, address)

    def changeEAA(self, newEAA):
        self.EAA = newEAA

class PG(Student):
    number_of_pgs = 0

    def __init__(self, id, pwd, type):
        self.research_area = ''
        PG.number_of_pgs += 1
        super().__init__(id, pwd, type)

    def setDetails(self, name, dob, gender, department, phone, year_of_admission, cgpa, hall, address, research_area):
        self.research_area = research_area
        super().setDetails(name, dob, gender, department, phone, year_of_admission, cgpa, hall, address)
#Teacher, Student, UG and PG have common super class Person, however attributes and methods specific toh these are also defined in the class definition 
#---------------------------------------------------------------------------------------------------------------------------------------------------------

# Neccessary GUI implementation starts from here

class UserSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("User System")

        self.user_id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_type_var = tk.StringVar()

        tk.Label(master, text="User ID:").pack()
        tk.Entry(master, textvariable=self.user_id_var).pack()

        tk.Label(master, text="Password:").pack()
        tk.Entry(master, textvariable=self.password_var, show="*").pack()

        tk.Label(master, text="User Type:").pack()
        user_types = ["Teacher", "UG Student", "PG Student"]
        for user_type in user_types:
            ttk.Radiobutton(master, text=user_type, variable=self.user_type_var, value=user_type).pack()

        tk.Button(master, text="Register", command=self.register_user).pack()
        tk.Button(master, text="Login", command=self.login_user).pack()
        self.failed_login_attempts = {}
# GUI itself is defined in form of a class, all the methods of this class are for GUI implementation

    def register_user(self):
        user_id = self.user_id_var.get()
        password = self.password_var.get()
        user_type = self.user_type_var.get()
        # taking entries for nacessary registration credentials

        if self.check_user_exists(user_id):
            messagebox.showerror("Registration Failed", "User ID already exists. Choose a different one.")
        elif not self.validate_password(password):
            messagebox.showerror("Registration Failed", '''Invalid password.
                                 a) It should be within 8-12 character long.\n
b) It should contain at least one upper case, one digit, and one lower case.\n
c) It should contains one or more special character(s) from the list [! @ # $ % & *]\n
d) No blank space will be allowed.''')# displaying instructions for password
        else:
            if user_type == "Teacher":
                new_user = Teacher(user_id, password, user_type)
            elif user_type == "UG Student":
                new_user = UG(user_id, password, user_type)
            elif user_type == "PG Student":
                new_user = PG(user_id, password, user_type)
            else:
                messagebox.showerror("Registration Failed", "Invalid user type.")
                return
            # messagebox.showinfo('hi','hello')
            self.save_user_to_csv(new_user)
            # different class object formation depending upon user type
            messagebox.showinfo("Registration Successful", "User registered successfully!")
    def validate_password(self, password):
        """
        Validate the password against specified criteria.
        Returns True if the password is valid, else False.
        """
        if not (8 <= len(password) <= 12):
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%&*]', password):
            return False
        if ' ' in password:
            return False
        return True #checking validation of password before any after registration
    def login_user(self):
        user_id = self.user_id_var.get()
        password = self.password_var.get()
        user_type = self.user_type_var.get()

        if not self.check_user_exists(user_id):
            messagebox.showerror("Login Failed", "User not registered.")
        else:
            # Check if there are consecutive failed login attempts
            attempts = self.failed_login_attempts.get(user_id, 0)

            if attempts >= 3:
                # Deactivate the account and show a message
                self.deactivate_user_account(user_id)
                messagebox.showinfo("Login Failed", "Account is deactivated.")
            elif self.check_credentials_match(user_id, password, user_type):
                # Reset failed login attempts on successful login
                self.failed_login_attempts[user_id] = 0
                messagebox.showinfo("Login Successful", "Welcome!")
                self.open_second_window(user_id)
            else:
                # Increment failed login attempts
                self.failed_login_attempts[user_id] = attempts + 1
                messagebox.showerror("Login Failed", "Incorrect credentials.")

    def deactivate_user_account(self, user_id):
        # Deactivate the user account by setting status to -1 in the CSV file
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = '-1'  # Update status to -1

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        # Additional actions can be added after deactivation if needed

    def open_second_window(self, user_id):
        second_window = tk.Toplevel(self.master)#created new window after login
        status = self.get_user_status(user_id)
        user_type = self.user_type_var.get()

        if user_type == "Teacher":
            if status == 0:
                self.create_teacher_profile(second_window, user_id)
            elif status == 1:
                self.update_teacher_profile(second_window, user_id)
        elif user_type == "UG Student":
            if status == 0:
                self.create_ug_profile(second_window, user_id)
            elif status == 1:
                self.update_ug_profile(second_window, user_id)
        elif user_type == "PG Student":
            if status == 0:
                self.create_pg_profile(second_window, user_id)
            elif status == 1:
                self.update_pg_profile(second_window, user_id)
        else:
            messagebox.showerror("Error", "Invalid user type.")
        deregister_button = tk.Button(second_window, text="Deregister", command=lambda: self.deregister_user(user_id, second_window))
        deregister_button.pack()
        # second window contatins different filled for different case of user type and user status
    def deregister_user(self, user_id, window):
        confirmation = messagebox.askyesno("Deregister User", "Are you sure you want to deregister your account?")
        if confirmation:
        # Remove user from the CSV file
            with open("user_data.csv", "r+", newline="") as file:
                lines = list(csv.reader(file))
                new_lines = [line for line in lines if line[0] != user_id]
                file.seek(0)
                file.truncate()  # Clear the file content
                writer = csv.writer(file)
                writer.writerows(new_lines)

            messagebox.showinfo("Deregistration Successful", "User deregistered successfully!")
            window.destroy()
        # You can also add additional actions after deregistration if needed
        else:
            messagebox.showinfo("Deregistration Canceled", "Deregistration process canceled.")


    def get_user_status(self, user_id):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return int(row[3])  # status is in the 4th column
        return -1

    def create_teacher_profile(self, window, user_id):
        tk.Label(window, text="Teacher Profile Creation").pack()

        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()

        tk.Label(window, text="Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()

        tk.Label(window, text="Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Label(window, text="Warden:").pack()
        warden_entry = tk.Entry(window)
        warden_entry.pack()

        tk.Label(window, text="Post:").pack()
        post_entry = tk.Entry(window)
        post_entry.pack()

        tk.Button(window, text="Save", command=lambda: self.save_teacher_profile(window, user_id,
                                                                                 name_entry.get(), dob_entry.get(),
                                                                                 gender_entry.get(), department_entry.get(),
                                                                                 phone_entry.get(), warden_entry.get(),
                                                                                 post_entry.get())).pack()
        # this function is responsible for profile setting of teacher type user

    def update_teacher_profile(self, window, user_id):
        tk.Label(window, text="Teacher Profile Update").pack()

        tk.Label(window, text="Password:").pack()
        pwd_entry = tk.Entry(window)
        pwd_entry.pack()
        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Button(window, text="Update", command=lambda: self.update_teacher_data(window, user_id,pwd_entry.get(),
                                                                                  name_entry.get(), phone_entry.get())).pack()
        # this function is responsible for updating certain fields of teacher type user

    def save_teacher_profile(self, window, user_id, name, dob, gender, department, phone, warden, post):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = '1'  # Update status to 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][9] = warden
                    lines[i][10] = post

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        messagebox.showinfo("Profile Update", "Teacher profile updated successfully!")
        window.destroy()#saving updated data

    def update_teacher_data(self, window, user_id,new_pwd, name, phone):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][1] = new_pwd
                    lines[i][4] = name
                    lines[i][8] = phone

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)# only few fields could be set while updating

        messagebox.showinfo("Profile Update", "Teacher profile updated successfully!")
        window.destroy()

    def create_ug_profile(self, window, user_id):
        tk.Label(window, text="UG Student Profile Creation").pack()

        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()

        tk.Label(window, text="Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()

        tk.Label(window, text="Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Label(window, text="Year of Admission:").pack()
        year_entry = tk.Entry(window)
        year_entry.pack()

        tk.Label(window, text="CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()

        tk.Label(window, text="Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()

        tk.Label(window, text="Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()

        tk.Label(window, text="EAA:").pack()
        eaa_entry = tk.Entry(window)
        eaa_entry.pack()

        tk.Button(window, text="Save", command=lambda: self.save_ug_profile(window, user_id,
                                                                            name_entry.get(), dob_entry.get(),
                                                                            gender_entry.get(), department_entry.get(),
                                                                            phone_entry.get(), year_entry.get(),
                                                                            cgpa_entry.get(), hall_entry.get(),
                                                                            address_entry.get(), eaa_entry.get())).pack()

    def update_ug_profile(self, window, user_id):
        tk.Label(window, text="UG Student Profile Update").pack()

        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Label(window, text="CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()

        tk.Label(window, text="Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()

        tk.Label(window, text="Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()

        tk.Button(window, text="Update", command=lambda: self.update_ug_data(window, user_id,
                                                                             name_entry.get(), phone_entry.get(),
                                                                             cgpa_entry.get(), hall_entry.get(),
                                                                             address_entry.get())).pack()

    def save_ug_profile(self, window, user_id, name, dob, gender, department, phone,
                        year_of_admission, cgpa, hall, address, EAA):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = '1'  # Update status to 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][11] = year_of_admission
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][15] = EAA

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        messagebox.showinfo("Profile Update", "UG student profile updated successfully!")
        window.destroy()

    def update_ug_data(self, window, user_id, name, phone, cgpa, hall, address):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][4] = name
                    lines[i][8] = phone
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        messagebox.showinfo("Profile Update", "UG student profile updated successfully!")
        window.destroy()

    def create_pg_profile(self, window, user_id):
        tk.Label(window, text="PG Student Profile Creation").pack()

        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="DOB:").pack()
        dob_entry = tk.Entry(window)
        dob_entry.pack()

        tk.Label(window, text="Gender:").pack()
        gender_entry = tk.Entry(window)
        gender_entry.pack()

        tk.Label(window, text="Department:").pack()
        department_entry = tk.Entry(window)
        department_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Label(window, text="Year of Admission:").pack()
        year_entry = tk.Entry(window)
        year_entry.pack()

        tk.Label(window, text="CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()

        tk.Label(window, text="Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()

        tk.Label(window, text="Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()

        tk.Label(window, text="Research Area:").pack()
        research_area_entry = tk.Entry(window)
        research_area_entry.pack()

        tk.Button(window, text="Save", command=lambda: self.save_pg_profile(window, user_id,
                                                                            name_entry.get(), dob_entry.get(),
                                                                            gender_entry.get(), department_entry.get(),
                                                                            phone_entry.get(), year_entry.get(),
                                                                            cgpa_entry.get(), hall_entry.get(),
                                                                            address_entry.get(), research_area_entry.get())).pack()

    def update_pg_profile(self, window, user_id):
        tk.Label(window, text="PG Student Profile Update").pack()

        tk.Label(window, text="Name:").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Phone:").pack()
        phone_entry = tk.Entry(window)
        phone_entry.pack()

        tk.Label(window, text="CGPA:").pack()
        cgpa_entry = tk.Entry(window)
        cgpa_entry.pack()

        tk.Label(window, text="Hall:").pack()
        hall_entry = tk.Entry(window)
        hall_entry.pack()

        tk.Label(window, text="Address:").pack()
        address_entry = tk.Entry(window)
        address_entry.pack()

        tk.Label(window, text="Research Area:").pack()
        research_area_entry = tk.Entry(window)
        research_area_entry.pack()

        tk.Button(window, text="Update", command=lambda: self.update_pg_data(window, user_id,
                                                                             name_entry.get(), phone_entry.get(),
                                                                             cgpa_entry.get(), hall_entry.get(),
                                                                             address_entry.get(),
                                                                             research_area_entry.get())).pack()

    def save_pg_profile(self, window, user_id, name, dob, gender, department, phone,
                        year_of_admission, cgpa, hall, address, research_area):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][3] = '1'  # Update status to 1
                    lines[i][4] = name
                    lines[i][5] = dob
                    lines[i][6] = gender
                    lines[i][7] = department
                    lines[i][8] = phone
                    lines[i][11] = year_of_admission
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][16] = research_area

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        messagebox.showinfo("Profile Update", "PG student profile updated successfully!")
        window.destroy()

    def update_pg_data(self, window, user_id, name, phone, cgpa, hall, address, research_area):
        with open("user_data.csv", "r+", newline="") as file:
            lines = list(csv.reader(file))

            for i, row in enumerate(lines):
                if row[0] == user_id:
                    lines[i][4] = name
                    lines[i][8] = phone
                    lines[i][12] = cgpa
                    lines[i][13] = hall
                    lines[i][14] = address
                    lines[i][16] = research_area

                    file.seek(0)
                    writer = csv.writer(file)
                    writer.writerows(lines)

        messagebox.showinfo("Profile Update", "PG student profile updated successfully!")
        window.destroy()

    def check_user_exists(self, user_id):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    return True
        return False
    # checks if a user exists, usefull for registeration and login user verifications

    def check_credentials_match(self, user_id, password, user_type):
        with open("user_data.csv", "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id and row[1] == password and row[2] == user_type:
                    return True
        return False
    #checks if credentaials matches during login

    def save_user_to_csv(self, user):
        with open("user_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if (user.type=='Teacher'):
                writer.writerow([user.user_id, user.password, user.type, user.status, user.name,
                                 user.dob, user.gender, user.department, user.phone, user.warden, user.post])
            elif (user.type=="UG Student"):
                writer.writerow([user.user_id, user.password, user.type, user.status, user.name,
                                 user.dob, user.gender, user.department, user.phone, user.year_of_admission,
                                 user.cgpa, user.hall, user.address.house, user.address.city,
                                 user.address.pincode, user.address.state, user.EAA])
            elif (user.type=="PG Student"):
                writer.writerow([user.user_id, user.password, user.type, user.status, user.name,
                                 user.dob, user.gender, user.department, user.phone, user.year_of_admission,
                                 user.cgpa, user.hall, user.address.house, user.address.city,
                                 user.address.pincode, user.address.state, user.research_area])
            else:
                messagebox.showerror("Save Error", "Invalid user type for saving.")
            # messagebox.showinfo('here','here')
            #save data of a perticular type user while registering, the fields which are not been taken as input are saved with defaul values.

# Execution starts here
if __name__ == "__main__":
    root = tk.Tk()
    app = UserSystemGUI(root)
    root.mainloop()
# here root should be called in order to initiate gui and its functionalities further.