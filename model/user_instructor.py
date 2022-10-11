from model.user import User
import re
import os
import random
import math
import matplotlib.pyplot as plt


class Instructor(User):
    """
    The Instructor class inherits from the User class.
    Class Instructor creates the basic template for Instructor

    Attributes
    -------
    id : integer
    user id
    username : string
    username
    password : string
    passwords not encrypted
    display_name : string
    full name
    job_title : string
    job title
    course_id_list : list
    list of course ids taught by one instructor

    Methods
    --------
    get_instructors():
    This method will extract instructor information from the given course data
    files.

    get_instructors_by_page()->tuple
    One positional argument: page. This method reads the user.txt file to retrieve
    all the instructor information.

     generate_instructor_figure1()->str
    Generate a graph that shows the top 10 instructors who teach the most
    courses.(any chart)
    """
    def __init__(self, uid=-1, username="", password=" ", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="instructor",
                 email="", display_name="", job_title="", course_id_list=[]):
        """
        Parameters
        ----------
        id : integer
        user id
        username : string
        username
        password : string
        passwords not encrypted
        """
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = "instructor"
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    def __str__(self):
        if len(self.course_id_list) == 0:
            course_list = ""
        else:
            course_list = str(self.course_id_list[0])
            if len(self.course_id_list) > 1:
                del self.course_id_list[0]
                for each in self.course_id_list:
                    course_list += "--" + str(each)
        return str(self.uid) + ";;;" + self.password + ";;;" + self.register_time + ";;;" + self.role + ";;;" +\
                   self.email + ";;;" + self.display_name + ";;;" + self.job_title + ";;;" + course_list

    def get_instructors(self):
        course_id = []
        instructor_id = []
        instructor_course = {}
        display_name = []
        instructor_username = []
        instructor_password = []
        instructor_email = []
        job_title = []
        course_path = 'data/source_course_files'
        course_folder = os.listdir(course_path)
        for path in course_folder:
            each_course_path = course_path + "/" + path
            each_course_folder = os.listdir(each_course_path)
            for each_file in each_course_folder:
                each_file_course_path = each_course_path + "/" + each_file
                each_file_course_folder = os.listdir(each_file_course_path)
                # This code gets each individual json file.
                for each_json in each_file_course_folder:
                    json_path = each_file_course_path + "/" + each_json
                    with open(json_path, 'r') as file:
                        for raw_line in file:
                            raw_course = re.split('"_class": "course"', raw_line)
                            del raw_course[0]
                            for each in raw_course:
                                # find pattern for course ID
                                regex_ID = r'"id": (\d+)'
                                IDs = re.findall(regex_ID, each)
                                course_id.append(IDs[0])
                                # find instructors that teach different course through instructor id
                                if IDs[1] in instructor_id:
                                    instructor_course[IDs[1]].append(IDs[0])
                                else:
                                    instructor_id.append(IDs[1])
                                    instructor_course[IDs[1]] = []
                                    instructor_course[IDs[1]].append(IDs[0])
                                    # find instructor name
                                    regex_display = r'"display_name": "(.+?)"'
                                    display = re.findall(regex_display, each)
                                    display_name.append(display[0])
                                    # find job title
                                    regex_job = r'"job_title": "(.+?)"'
                                    job = re.findall(regex_job, each)
                                    job_title.append(job[0])
                                    # create username
                                    t = []
                                    for name in display:  # replace white space with underscore
                                        re_whitespace = name.replace(" ", "_")
                                        alpha = re.compile('[^a-zA-Z_]')
                                        t.append(alpha.sub('', re_whitespace).lower())
                                    instructor_username.append(t[0])
                                    instructor_email.append(t[0] + "@gmail.com")
                                    # create instructor password use super() after test
                                    password = super().encrypt_password(IDs[1])
                                    instructor_password.append(password)
        # create string file for user_instructor.txt file
        user_instructor_txt = ''
        for i in range(0, len(instructor_username)):
            testing = instructor_course[instructor_id[i]]
            c_ids = testing[0]
            if len(testing) > 1:
                for a in range(1, len(testing)):
                    c_ids += "--" + testing[a]
            c = instructor_id[i] + ";;;" + instructor_username[i] + ";;;" + instructor_password[i] + ";;;" \
                + self.register_time + ";;;" + self.role + ";;;" + instructor_email[i] + ";;;" + display_name[i] \
                + ";;;" + job_title[i] + ";;;" + c_ids + "\n"
            user_instructor_txt += c
        with open('data/user.txt', 'a') as file:
            file.write(user_instructor_txt)

    def get_instructors_by_page(self, page):
        # create a dictionary of num:instructor object
        info_num = 1
        Instructor_dic = {}
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "instructor":
                        if len(raw) < 9:
                            c_id_list = []
                        else:
                            c_id_list = re.split('--', raw[8])
                        Instructor_obj = Instructor(uid=int(raw[0]), username=raw[1], password=raw[2], register_time=raw[3],
                                                    role=raw[4], email=raw[5], display_name=raw[6], job_title=raw[7],
                                                    course_id_list=c_id_list)
                        Instructor_dic[info_num] = Instructor_obj
                        info_num += 1
        # create list for retrieving data based on total pages
        total = len(Instructor_dic)
        if total % 20 != 0:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        # if page greater than total page go to max, if negative go 1 page
        if page > total_page:
            page = total_page
        if page <= 0:
            page = 1
        num_list = list(range(1, 21))
        if page < total_page:
            num_list = list(range(page * 20 - 19, page * 20 + 1))
        elif page == total_page:
            num_list = list(range(page * 20 - 19, total + 1))
        # create list of course object based on num_list
        instructor_list = []
        if total != 0:
            for each in num_list:
                instructor_list.append(Instructor_dic[each])
        return (instructor_list, total_page, total)

    def generate_instructor_figure1(self):
        instructor_dic = {}
        # create a dictionary of num:instructor object
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "instructor":
                        if len(raw) > 6:
                            display_name = raw[6]
                            if len(raw) < 9:
                                c_id_list = []
                            else:
                                c_id_list = re.split('--', raw[8])
                            rank = len(c_id_list)
                            instructor_dic[display_name] = rank
        # sort the dictionary
        top_instructor = sorted(instructor_dic.items(), key=lambda x: x[1], reverse=True)
        top_10_instructor = top_instructor[0:10]
        graph_dic = {}
        for each in top_10_instructor:
            le = re.split(' ', each[0])
            if len(le) > 3:
                del le[3:]
                key = " ".join(le)
            else:
                key = each[0]
            value = each[1]
            graph_dic[key] = value
        # plot the graph
        plt.clf()
        plt.title("Top 10 ranked Instructors that teach the most course")
        plt.ylabel("Number of Courses")
        plt.xlabel("Name of Instructor")
        # Seperate instructor with different color
        plt.bar(*zip(*graph_dic.items()))
        plt.xticks(rotation=45, fontsize=5)
        plt.savefig('static/img/instructor_figure1')
        return "This bar plot demonstrates the the top 10 ranked instructors that teach the most courses " \
               "in the user.txt"
