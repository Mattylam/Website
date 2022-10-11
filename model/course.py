import re
import os
import random
import matplotlib.pyplot as plt

class Course:
    """
        Attributes
        -------
        course_id : integer
        course_title : string
        course_image_100x100 : string
        course_headline : string
        course_num_subscribers: integer
        course_avg_rating: float
        course_content_length: integer

        Methods
        --------
         find_course_by_title_keyword(keyword)
        This method has a positional argument keyword(str). Based on the given keyword, it
        searches the course title of all courses in the course.txt file to find the result. All the
        result courses will be created as a course object and added into a result list.
        The list wil be returned

         find_course_by_id(course_id)
        This method has a positional argument course id(int or str). A course object will be returned. If
        not found, return None.

        find_course_by_instructor_id(instructor_id)
        This method has a positional argument instructor id(int or str). Based on the
        instructor id, a list of course objects will be generated and returned. If not found, return an empty list.

        courses_overview()
        This method returns a string that shows the total number of courses.
        """

    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="", subcategory_description="",
                 subcategory_url="", course_id=-1, course_title="", course_url="", num_of_subscribers=0,
                 avg_rating=0.0, num_of_reviews=0):
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    def __str__(self):
        return self.category_title + ";;;" + str(self.subcategory_id) + ";;;" + self.subcategory_title + ";;;" + \
               self.subcategory_description + ";;;" + self.subcategory_url + ";;;" + str(self.course_id) + ";;;" + \
               self.course_title + ";;;" + self.course_url + ";;;" + str(self.num_of_subscribers) + ";;;" + \
               str(self.avg_rating) + ";;;" + str(self.num_of_reviews)

    def get_courses(self):
        course_path = 'data/source_course_files'
        course_folder = os.listdir(course_path)
        course_txt = ''
        for path in course_folder:
            each_course_path = course_path + "/" + path
            each_course_folder = os.listdir(each_course_path)
            category_list = re.split('_', path)
            category_title = category_list[2]
            for each_file in each_course_folder:
                each_file_course_path = each_course_path + "/" + each_file
                each_file_course_folder = os.listdir(each_file_course_path)
                # This code gets each individual json file.
                for each_json in each_file_course_folder:
                    json_path = each_file_course_path + "/" + each_json
                    with open(json_path, 'r') as file:
                        for raw_line in file:
                            raw_line = raw_line.strip("\n")
                            raw_course = re.split('"_class": "course"', raw_line)
                            subcategory_id = []
                            subcategory_title = []
                            subcategory_description = []
                            subcategory_url = []
                            course_id = []
                            course_title = []
                            course_url = []
                            num_of_subscriber = []
                            course_avg_rating = []
                            num_of_reviews = []
                            # find pattern for sub id
                            regex_sub_ID = r'"id": (\d+)'
                            sub_ID = re.findall(regex_sub_ID, raw_course[0])
                            subcategory_id.append(sub_ID[0])
                            # find pattern for sub title
                            regex_sub_title = r'"title": "(.+?)"'
                            sub_title = re.findall(regex_sub_title, raw_course[0])
                            subcategory_title.append(sub_title[0])
                            # find pattern for description
                            regex_description = r'"description": (.+?),'
                            description = re.findall(regex_description, raw_course[0])
                            subcategory_description.append(description[0].replace("}]", ""))
                            # find pattern for course url
                            regex_sub_url = r'"url": (.+?),'
                            sub_url = re.findall(regex_sub_url, raw_course[0])
                            subcategory_url.append(sub_url[0])
                            del raw_course[0]
                            for each in raw_course:
                                # find pattern for course ID
                                regex_ID = r'"id": (\d+)'
                                IDs = re.findall(regex_ID, each)
                                course_id.append(IDs[0])
                                # find pattern for course title
                                regex_title = r'"title": "(.+?)"'
                                titles = re.findall(regex_title, each)
                                course_title.append(titles[0])
                                # find pattern for course url
                                regex_url = r'"url": "(.+?)"'
                                url = re.findall(regex_url, each)
                                course_url.append(url[0])
                                # find pattern for subscriber
                                regex_sub = r'"num_subscribers": (\d+)'
                                subscriber = re.findall(regex_sub, each)
                                num_of_subscriber.append(subscriber[0])
                                # find pattern for avg of rating
                                regex_rating = r'"avg_rating": (.+?),'
                                rating = re.findall(regex_rating, each)
                                course_avg_rating.append(rating[0])
                                # find pattern for num of reviews
                                regex_review = r'"num_reviews": (\d+)'
                                review = re.findall(regex_review, each)
                                num_of_reviews.append(review[0])
                        # create string file for course.txt file
                        for i in range(0, len(course_id)):
                            c = category_title + ";;;" + subcategory_id[0] + ";;;" + subcategory_title[0] + ";;;" + \
                                subcategory_description[0] + ";;;" \
                                + subcategory_url[0] + ";;;" + course_id[i] + ";;;" + course_title[i] + ";;;" + \
                                course_url[i] \
                                + ";;;" + num_of_subscriber[i] + ";;;" + course_avg_rating[i] + ";;;" + num_of_reviews[
                                    i] + "\n"
                            course_txt += c
        # make course txt one string file
        f_out = open('data/course.txt', mode='w')
        f_out.write(course_txt)
        f_out.close()

    def clear_course_data(self):
        f_out = open('data/course.txt', mode='w')
        f_out.write("")
        f_out.close()

    def generate_page_num_list(self, page, total_pages):
        if page <= 5 and page > 0:
            num_list = list(range(1, 10))
        elif page > 5 and page < (total_pages - 4):
            num_list = list(range(page - 4, page + 5))
        elif page >= total_pages - 4:
            num_list = list(range(total_pages - 8, total_pages + 1))
        else:
            print("invalid input")
        return num_list

    def get_courses_by_page(self, page):
        # create a dictionary of num:course object
        info_num = 1
        course_dic = {}
        with open('data/course.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                course_obj = Course(category_title=raw[0], subcategory_id=int(raw[1]), subcategory_title=raw[2],
                                    subcategory_description=raw[3], subcategory_url=raw[4], course_id=int(raw[5]),
                                    course_title=raw[6], course_url=raw[7], num_of_subscribers=int(raw[8]),
                                    avg_rating=float(raw[9]), num_of_reviews=int(raw[10]))
                course_dic[info_num] = course_obj
                info_num += 1
        # create list for retrieving data based on total pages
        total = len(course_dic)
        if total % 20 != 0:
            total_page = total // 20 + 1
        else:
            total_page = total // 20
        # if page greater than total page go to max, if negative go 1 page
        if page > total_page:
            page = total_page
        if page <= 0:
            page = 1
            total_page = 1
        num_list = list(range(1, 21))
        if page < total_page:
            num_list = list(range(page * 20 - 19, page * 20 + 1))
        elif page == total_page:
            num_list = list(range(page * 20 - 19, total + 1))
        # create list of course object based on num_list
        course_list = []
        for a in num_list:
            course_list.append(course_dic[a])
        return (course_list, page, total_page)

    def delete_course_by_id(self, temp_course_id):
        delete_line = ""
        with open('data/course.txt', 'r') as file:
            # save whole text
            lines = file.readlines()
        with open('data/course.txt', 'r') as file:
            # search for student string in user.txt
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 5:
                    uid = int(raw[5])
                    if temp_course_id == uid:
                        delete_line = line
                        break
        if delete_line != "":
            # delete line based on course id
            with open('data/course.txt', 'w') as new_file:
                for line in lines:
                    if line.strip("\n") != delete_line.strip("\n"):
                        new_file.write(line)
            # delete course id from user.txt
            # find instructor that teach this course
            delete_ins = ""
            delete_user_line = ""
            with open('data/user.txt', 'r') as file:
                for line in file:
                    raw = re.split(';;;', line)
                    if len(raw) > 4:
                        if raw[4] == "instructor":
                            if len(raw) == 9:
                                c_id_list = re.split('--', raw[8])
                                for each in c_id_list:
                                    if int(each) == temp_course_id:
                                        delete_user_line = line
                                        c_id_list.remove(each)
                                        c_id = "--".join(c_id_list)
                                        raw[8] = c_id
                                        delete_ins = ";;;".join(raw)
                                        break
            # save whole test
            with open('data/user.txt', 'r') as file:
                # save whole text
                user_lines = file.readlines()
            # replace that line 
                # delete line based on course id
            with open('data/user.txt', 'w') as n_file:
                for line in user_lines:
                    if line.strip("\n") != delete_user_line.strip("\n"):
                        n_file.write(line)
                    else:
                        n_file.write(delete_ins + "\n")
            return True
        else:
            return False

    def get_course_by_course_id(self, temp_course_id):
        check = False
        course_obj = Course()
        with open('data/course.txt', 'r') as file:
            # search for student string in user.txt
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 5:
                    uid = int(raw[5])
                    if temp_course_id == uid:
                        check = True
                        course_obj = Course(category_title=raw[0], subcategory_id=int(raw[1]), subcategory_title=raw[2], 
                                            subcategory_description=raw[3], subcategory_url=raw[4], course_id=int(raw[5]),
                                            course_title=raw[6], course_url=raw[7], num_of_subscribers=int(raw[8]),
                                            avg_rating=float(raw[9]), num_of_reviews=int(raw[10]))
                        num_of_subscribers = int(raw[8])
                        avg_rating = float(raw[9])
                        num_of_reviews = int(raw[10])
                        break
        if check:
            if num_of_subscribers > 100000 and avg_rating > 4.5 and num_of_reviews > 10000:
                comment = "Top Course"
            elif num_of_subscribers > 50000 and avg_rating > 4.0 and num_of_reviews > 5000:
                comment = "Popular Course"
            elif num_of_subscribers > 10000 and avg_rating > 3.5 and num_of_reviews > 1000:
                comment = "Good Course"
            else:
                comment = "General Course"
        else:
            comment = "Not Found Course"
        return (course_obj, comment)

    def get_course_by_instructor_id(self, instructor_id):
        c_id_list = []
        with open('data/user.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 4:
                    if raw[4] == "instructor":
                        if int(instructor_id) == int(raw[0]):
                            if len(raw) == 9:
                                c_id_list = re.split('--', raw[8])
                                break
        if len(c_id_list) > 20:
            del c_id_list[20:]
        total_course = len(c_id_list)
        course_obj_list = []
        with open('data/course.txt', 'r') as file:
            for course_id in c_id_list:
                temp_course_id = int(course_id)
                # search for student string in user.txt
                for line in file:
                    line = line.strip("\n")
                    raw = re.split(';;;', line)
                    if len(raw) > 5:
                        uid = int(raw[5])
                        if temp_course_id == uid:
                            course_obj = Course(category_title=raw[0], subcategory_id=int(raw[1]), subcategory_title=raw[2], 
                                                subcategory_description=raw[3], subcategory_url=raw[4], course_id=int(raw[5]),
                                                course_title=raw[6], course_url=raw[7], num_of_subscribers=int(raw[8]),
                                                avg_rating=float(raw[9]), num_of_reviews=int(raw[10]))
                            course_obj_list.append(course_obj)
                            break
        return (course_obj_list, total_course)
            

    def generate_course_figure1(self):
        subcategory_dic = {}
        subcategory_title_list = []
        with open('data/course.txt', 'r') as file:
            for line in file:
                line = line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 5:
                    if raw[2] in subcategory_title_list:
                        subcategory_dic[raw[2]] += int(raw[8])
                    else:
                        subcategory_title_list.append(raw[2])
                        subcategory_dic[raw[2]] = int(raw[8])
        # sort the dictionary
        top_sub_category = sorted(subcategory_dic.items(), key=lambda x: x[1], reverse=True)
        top_10_sub_category = top_sub_category[0:10]
        y0 = []
        x0 = []
        for each in top_10_sub_category:
            le = re.split(' ', each[0])
            if len(le) > 3:
                del le[3:]
                key = " ".join(le)
            else:
                key = each[0]
            x0.append(key)
            value = each[1]
            y0.append(value)
        # plot the graph
        plt.clf()
        plt.title("Top 10 subcategory with the most number of subscribers")
        plt.ylabel("Number of subscribers")
        plt.xlabel("Subcategory Titles")
        # Seperate instructor with different color
        plt.bar(x0,y0, color=['black', 'red', 'green', 'blue', 'cyan'])
        plt.xticks(rotation=45, fontsize=5)
        # plt.show()
        plt.savefig('static/img/course_figure1')
        return "This bar plot demonstrates the top 10 subcategory with the most number of subscribers "

    def generate_course_figure2(self):
        rating_dic = {}
        with open('data/course.txt', 'r') as file:
            for line in file:
                line.strip("\n")
                raw = re.split(';;;', line)
                num_of_reviews = int(raw[10])
                if num_of_reviews > 50000:
                    course_title = raw[6]
                    avg_rating = float(raw[9])
                    rating_dic[course_title] = avg_rating
        # sort the dictionary
        low_rating = sorted(rating_dic.items(), key=lambda x: x[1])
        top_10_low_rating = low_rating[0:10]
        y = []
        x = []
        for each in top_10_low_rating:
            le = re.split(' ', each[0])
            if len(le) > 3:
                del le[3:]
                key = " ".join(le)
            else:
                key = each[0]
            x.append(key)
            value = each[1]
            y.append(value)
        # plot the graph
        plt.clf()
        plt.title("Top 10 courses with the lowest rating")
        plt.ylabel("Rating")
        plt.xlabel("Course Title")
        # Seperate instructor with different color
        plt.scatter(x, y)
        # plt.show()
        plt.xticks(rotation=45, fontsize=5)
        plt.savefig('static/img/course_figure2')
        return "This scatter plot demonstrates the Top 10 courses with the lowest rating "


    def generate_course_figure3(self):
        rating_dic1 = {}
        with open('data/course.txt', 'r') as file:
            for line in file:
                line.strip("\n")
                raw = re.split(';;;', line)
                num_of_subscribers = int(raw[8])
                if num_of_subscribers > 10000 and num_of_subscribers < 100000:
                    avg_rating = float(raw[9])
                    rating_dic1[avg_rating] = num_of_subscribers
        # sort the dictionary
        low_rating = sorted(rating_dic1.items(), key=lambda x: x[1])
        y1 = []
        x1 = []
        for each in low_rating:
            key = each[1]
            value = each[0]
            x1.append(key)
            y1.append(value)
        # plot the graph
        plt.clf()
        plt.title("Avg rating distribution of courses from 100000 to 10000")
        plt.ylabel("Rating")
        plt.xlabel("Number of subscribers")
        # Seperate instructor with different color
        plt.scatter(x1, y1)
        # plt.show()
        plt.savefig('static/img/course_figure3')
        return "This scatter plot demonstrates Avg rating distribution of courses from 100000 to 10000 "

    def generate_course_figure4(self):
        category_dic = {}
        category_title_list = []
        with open('data/course.txt', 'r') as file:
            for line in file:
                line.strip("\n")
                raw = re.split(';;;', line)
                category_title = raw[0]
                if category_title in category_title_list:
                    category_dic[category_title] += 1
                else:
                    category_title_list.append(category_title)
                    category_dic[category_title] = 1
        # sort the dictionary
        low_rating = sorted(category_dic.items(), key=lambda x: x[1], reverse=True)
        labels = []
        sizes = []
        for each in low_rating:
            le = re.split(' ', each[0])
            if len(le) > 3:
                del le[3:]
                key = " ".join(le)
            else:
                key = each[0]
            value = each[1]
            labels.append(key)
            sizes.append(value)
        # plot the graph
        plt.clf()
        fig1, ax1 = plt.subplots()
        myexplode = [0, 0.2, 0, 0]
        plt.title("Pie chart of all categories in terms of number of courses")
        ax1.pie(sizes, labels=labels, explode=myexplode, shadow=True, startangle=90)
        # plt.show()
        plt.savefig('static/img/course_figure4')
        return "This scatter plot demonstrates Pie chart of all categories in terms of number of courses"

    def generate_course_figure5(self):
        course_review_dic = {}
        course_review_dic['Number of courses with no review'] = 0
        course_review_dic['Number of courses with review'] = 0
        with open('data/course.txt', 'r') as file:
            for line in file:
                raw = re.split(';;;', line)
                num_of_reviews = int(raw[10])
                if num_of_reviews > 0:
                    course_review_dic['Number of courses with review'] += 1
                else:
                    course_review_dic['Number of courses with no review'] += 1
        x2 = list(course_review_dic.keys())
        y2 = list(course_review_dic.values())
        # plot the graph
        plt.clf()
        plt.title("Number of courses with review vs no review")
        plt.ylabel("Number of courses")
        # Seperate instructor with different color
        plt.bar(x2,y2)
        # plt.show()
        plt.savefig('static/img/course_figure5')
        return "This bar plot demonstrates Number of courses with review vs no review "

    def generate_course_figure6(self):
        subcategory_dic = {}
        subcategory_title_list = []
        with open('data/course.txt', 'r') as file:
            for line in file:
                line.strip("\n")
                raw = re.split(';;;', line)
                if len(raw) > 5:
                    if raw[2] in subcategory_title_list:
                        subcategory_dic[raw[2]] += 1
                    else:
                        subcategory_title_list.append(raw[2])
                        subcategory_dic[raw[2]] = 0
        # sort the dictionary
        top_sub_category = sorted(subcategory_dic.items(), key=lambda x: x[1])
        top_10_sub_category = top_sub_category[0:10]
        y = []
        x = []
        for each in top_10_sub_category:
            le = re.split(' ', each[0])
            if len(le) > 3:
                del le[3:]
                key = " ".join(le)
            else:
                key = each[0]
            x.append(key)
            value = each[1]
            y.append(value)
        # plot the graph
        plt.clf()
        plt.title("Top 10 subcategory with the least courses")
        plt.ylabel("Number of courses")
        plt.xlabel("Subcategory Titles")
        # Seperate instructor with different color
        plt.bar(x,y, color=['black', 'red', 'green', 'blue', 'cyan'])
        # plt.show()
        plt.xticks(rotation=45, fontsize=5)
        plt.savefig('static/img/course_figure6')
        return "This bar plot demonstrates the Top 10 subcategory with the least courses"















