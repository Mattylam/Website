import re
import os
import random
import math
from datetime import datetime
from lib.helper import get_day_from_timestamp
# I got this function from helper.py
"""def get_day_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).day"""


class User:
    """
        Class User creates the basic template for all users
        User class handles the fundamental methods of all users. The User class is the parent
        class of Admin, Instructor and Student classes.

        Attributes
        -------
            id : integer
            user id
            username : string
            username
            password : string
            passwords not encrypted

        Methods
        --------
            generate_unique_user_id(self):
            This method checks the files user_admin.txt, user_instructor.txt and user_student.txt
            to generate a 10 digits integer. If files do not exist this function will not check these files

            encryption(input_password):
            This method encrypts the input_password to a string that is difficult to read by humans

            authenticate_user():
            Two positional arguments - username and password. This method is used to
            check whether username and password can be matched with users saved in
            user.txt data file. If matched, this method will retrieve the user information
            from user.txt file and return a tuple (True, user_info_string), otherwise return
            (False, “”).

            check_username_exist():
            One positional argument - username. This method is to check whether the
            given username exists in the user.txt data file. If it exists, return True,
            otherwise return False.

             generate_unique_user_id():
            This method is used to generate and return a 6 digit unique user id which is
            not in the user.txt file.
            encrypt_password()->str.
            One positional argument - password. For a given password, you are required
            to encrypt the string.

            register_user()->bool.
            Five positional arguments - username, password, email, register_time, role.

            date_conversion()-> str.
            One positional argument - register_time. The given register_time will be a unix
            epoch timestamp (milli seconds) and it needs to be converted to format
            “year-month-day_hour:minute:second.milliseconds”.

            validate_username()-> bool.
            One positional argument - username. The username can only be letters or
            underscore. If not, return False.

            validate_password()-> bool.
            One positional argument - password. The length of password must be greater
            than or equal to 5. If not, return False.

            validate_email()-> bool.
            One positional argument - email. Use regex expressions to check whether the
            email address is valid or not. The email should end with “.com”, contain “@”,
            and have length greater than 8. If not, return False.

            clear_user_data() no return.
            This method will remove all the data in the user.txt file.
        """
    current_login_user = None
    
    def __init__(self, uid=-1, username="", password=" ", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role=""):
        """
        Parameters
        ----------
        id : integer
        user id
        username : string
        username
        password : string
        password
        register_time: string

        role: string

        """
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        role_list = ["admin", "instructor", "student"]
        if role in role_list:
            self.role = role

    def __str__(self):
        return str(self.uid) + ";;;" + self.password + ";;;" + self.register_time + ";;;" + self.role

    def validate_username(self, username):
        check = False
        if re.match("^[A-Za-z_]*$", username):
            check = True
        return check

    def validate_password(self, password):
        check = False
        if len(password) >= 5:
            check = True
        return check

    def validate_email(self, email):
        check = False
        if len(email) >= 8:
            if re.match(r"[\w\.]+@[\w\.-]+", email):
                if email[-4:] == ".com":
                    check = True
        return check

    def clear_user_data(self):
        f_out = open('data/user.txt', mode='w')
        f_out.write("")
        f_out.close()

    def authenticate_user(self, username, password):
        check = False
        user_info = ""
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 2:
                    data_username = raw[1]
                    data_password = raw[2]
                    en_password = self.encrypt_password(password)
                    if data_username == str(username) and data_password == en_password:
                        user_info = line
                        check = True
                        break
        return (check, user_info)

    def check_username_exist(self, username):
        check = False
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 1:
                    data_username = raw[1]
                    if data_username == username:
                        check = True
                        break
        return check

    def generate_unique_user_id(self):
        id_list = []
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if raw[0].isdigit():
                    id_list.append(int(raw[0]))
        new_user_id = random.randint(100000, 1000000)
        while new_user_id in id_list:
            new_user_id = random.randint(100000, 1000000)
        return new_user_id

    def encrypt_password(self, password):
        """
         This method encrypts the input_password to a string that is difficult to read by humans

         a : integer

         returns a string of encrypted password
         """
        # the goal of this function is to encrypt password
        a = str(password)
        # the following function defines the length and calculates the characters used.
        password_len = len(a)
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        first = len(all_punctuation) % password_len
        firstcharacter = all_punctuation[first]
        secondcharacter = all_punctuation[password_len % 5]
        thirdcharacter = all_punctuation[password_len % 10]
        # encrypt is defined as ^^^ because it is the requirement to add ^^^ in all passwords.
        encrypt = "^^^"
        # for function runs with step size 3, because the conditions loops every three characters.
        for i in range(0, len(a), 3):
            if i < len(a):
                # this if condition makes sure i is within the range of input
                encrypt += firstcharacter
                encrypt += a[i]
                encrypt += firstcharacter
                if i + 1 < len(a):
                    encrypt += secondcharacter * 2
                    encrypt += a[i + 1]
                    encrypt += secondcharacter * 2
                    if i + 2 < len(a):
                        encrypt += thirdcharacter * 3
                        encrypt += a[i + 2]
                        encrypt += thirdcharacter * 3
        encrypt += "$$$"
        return encrypt

    def register_user(self, username, password, email, register_time, role):
        if self.check_username_exist(username):
            return False
        else:
            new_user_id = self.generate_unique_user_id()
            timestamp = self.date_conversion(register_time)
            encrypt_password = self.encrypt_password(password)
            if role == "instructor":
                display_name = ""
                job_title = ""
                course_id_list = ""
                register = str(new_user_id) + ";;;" + username + ";;;" + encrypt_password + ";;;" + timestamp + ";;;" +\
                           role + ";;;" + email + ";;;" + display_name + ";;;" + job_title + ";;;" + course_id_list
            else:
                register = str(new_user_id) + ";;;" + username + ";;;" + encrypt_password + ";;;" + timestamp + ";;;" +\
                           role + ";;;" + email
            with open('data/user.txt', 'a') as file:
                file.write("\n" + register)
                return True

    def date_conversion(self, register_time):
        # get date
        if len(str(register_time)) > 10:
            register_time = str(register_time)[:10]
        register_time = int(register_time)
        date = str(get_day_from_timestamp(register_time))
        # convert to GMT+11
        register_time += (3600 * 11)
        # get HH:MM:SS
        hh = register_time % (24 * 60 * 60)
        hours = hh // 3600
        hh_minutes = (hh / 3600 - hours) * 60
        seconds, minute = math.modf(hh_minutes)
        seconds *= 60
        time = str(hours) + ":" + str(int(minute)) + ":" + str(int(round(seconds)))
        # years
        current_year = 1970
        days = register_time // (24 * 60 * 60)
        # Calculating current year
        while days >= 365:
            # leap year
            if current_year % 400 == 0 or (current_year % 4 == 0 and current_year % 100 != 0):
                days -= 366

            else:
                days -= 365

            current_year += 1
        year = str(current_year)
        # Calculate Month
        extraDays = days + 1
        month = 0
        index = 0
        # leap year
        if current_year % 400 == 0 or (current_year % 4 == 0 and current_year % 100 != 0):
            daysOfMonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            daysOfMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        while True:
            if extraDays - daysOfMonth[index] < 0:
                break
            month += 1
            extraDays -= daysOfMonth[index]
            index += 1
        # current month
        if extraDays > 0:
            month += 1
        ans = date + "/" + str(month) + "/" + year + " " + time
        return ans

