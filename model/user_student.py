from model.user import User
import re
import os
import random
import math


class Student(User):
    """
    Student class inherits from the User class
    Class Student creates the basic template for Students

    Attributes
    -------
    uid : integer
    user id
    username : string
    username
    password : string
    passwords not encrypted
    user_title : string
    full name
    email : string
    email

    Methods
    --------
     get_students_by_page()->tuple.
        One positional argument: page. This method reads the user.txt file to retrieve
        all the student information.

    view_reviews(args=[])
    This method prints out the review this student wrote.

    get_student_by_id()->Student object
    One positional argument id. This method returns a student object by retrieving
    the id from the user.txt file.

    delete_student_by_id()->bool
    One positional argument id. This method deletes a student item from the
    user.txt file based on the given id.

    """
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student",
                 email=""):
        """
                Parameters
                ----------
                uid : integer
                user id
                username : string
                username
                password : string
                passwords not encrypted
                user_title : string
                full name
                email : string
                email
                """
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role
        self.email = email

    def __str__(self):
        return str(self.uid) + ";;;" + self.password + ";;;" + self.register_time + ";;;" \
               + self.role + ";;;" + self.email

    def get_students_by_page(self, page):
        # create a dictionary of num:instructor object
        info_num = 1
        students_dic = {}
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "student":
                        students_obj = Student(uid=int(raw[0]), username=raw[1], password=raw[2], register_time=raw[3],
                                               role=raw[4], email=raw[5])
                        students_dic[info_num] = students_obj
                        info_num += 1
        # create list for retrieving data based on total pages
        total = len(students_dic)
        num_list = list(range(1, 21))
        if total % 20 != 0:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        # if page greater than total page go to max, if negative go 1 page
        if page > total_page:
            page = total_page
        if page <= 0:
            page = 1
        if page < total_page:
            num_list = list(range(page * 20 - 19, page * 20 + 1))
        elif page == total_page:
            num_list = list(range(page * 20 - 19, total + 1))
        # create list of course object based on num_list
        students_list = []
        if total != 0:
            for each in num_list:
                students_list.append(students_dic[each])
        return (students_list, total_page, total)

    def get_student_by_id(self, student_id):
        # create a dictionary of num:instructor object
        students_obj = Student()
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "student":
                        uid = int(raw[0])
                        if student_id == uid:
                            students_obj = Student(uid=int(raw[0]), username=raw[1], password=raw[2], register_time=raw[3],
                                               role=raw[4], email=raw[5])
                            break
        return students_obj


    def delete_student_by_id(self, student_id):
        # create a dictionary of num:instructor object
        delete_line = ""
        with open('data/user.txt', 'r') as file:
            # save whole text
            lines = file.readlines()
        with open('data/user.txt', 'r') as file:
            # search for student string in user.txt
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "student":
                        uid = int(raw[0])
                        if int(student_id) == int(uid):
                            delete_line = line
                            break
        if delete_line != "":
            with open('data/user.txt', 'w') as new_file:
                for line in lines:
                    if line.strip("\n") != delete_line.strip("\n"):
                        new_file.write(line)
            return True
        else:
            return False


