import re
from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(user_info):
    raw = re.split(';;;', user_info[1])
    uid = int(raw[0])
    username = raw[1]
    password = raw[2]
    register_time = raw[3]
    role = raw[4]
    if role == "admin":
        return Admin(uid=uid, username=username, password=password, register_time=register_time, role=role)
    elif role == "student":
        email = raw[5]
        return Student(uid=uid, username=username, password=password, register_time=register_time, role=role,
                       email=email)
    elif role == "instructor":
        email = raw[5]
        display_name = raw[6]
        job_title = raw[7]
        if len(raw) < 9:
            c_id_list = []
        else:
            c_id_list = re.split('--', raw[8])
        return Instructor(uid=uid, username=username, password=password, register_time=register_time, role=role,
                          email=email, display_name=display_name, job_title=job_title, course_id_list=c_id_list)


# use @user_page.route("") for each page url
@user_page.route("/login")
def login():
    return render_template("00login.html")


@user_page.route("/login", methods=['POST'])
def login_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    if model_user.validate_username(username) & model_user.validate_password(password):
        user_info = model_user.authenticate_user(username, password)
        if user_info[0]:
            User.current_login_user = generate_user(user_info)
            return render_result(msg="login success")
    return render_result(msg="login error")


@user_page.route("/logout")
def logout():
    User.current_login_user = None
    return render_template("01index.html")


@user_page.route("/register")
def register():
    return render_template("00register.html")


@user_page.route("/register", methods=['POST'])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    email = req["email"] if "email" in req else "null"
    register_time = req["register_time"] if "register_time" in req else "0"
    role = req["role"] if "role" in req else "null"
    check = model_user.validate_username(username)
    if check:
        if model_user.validate_password(password):
            if model_user.validate_email(email):
                model_user.register_user(username, password, email, register_time, role)
                return render_result(msg="Register successfully")
            else:
                return render_err_result(msg="Invalid email")
        else:
            return render_err_result(msg="Invalid password")
    else:
        return render_err_result(msg="Invalid Username")


@user_page.route("/student-list")
def student_list():
    if User.current_login_user is not None:  # check login user
        context = {}
        req = request.values
        page = req['page'] if "page" in req else 1
        page = int(page)
        # get values for one_page_course_list, total_pages, total_num
        get_tuple = model_student.get_students_by_page(page)
        one_page_student_list = get_tuple[0]
        total_pages = get_tuple[1]
        total_num = get_tuple[2]
        # get values for page_num_list
        page_num_list = model_course.generate_page_num_list(page=page, total_pages=total_pages)
        print(one_page_student_list)

        context['one_page_student_list'] = one_page_student_list
        context['total_pages'] = total_pages
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num

        # add "current_user_role" to context
        role = User.current_login_user.role
        context['current_user_role'] = role
        return render_template("10student_list.html", **context)
    else:
        return redirect(url_for("index_page.index"))



@user_page.route("/student-delete")
def student_delete():
    req = request.values
    id = req['id'] if "id" in req else 0
    delete = model_student.delete_student_by_id(id)
    if delete:
        return redirect(url_for("user_page.student_list"))
    else:
        return redirect(url_for("index_page.index"))


@user_page.route("/student-info")
def student_info():
    context = {}
    if User.current_login_user.role == "admin":  # check login user
        req = request.values
        id = req['id'] if "id" in req else -1
        id = int(id)
        if id == -1:
            student_obj = Student()
        else:
            student_obj = model_student.get_student_by_id(id)
        context['student_obj'] = student_obj
        return render_template("11student_info.html", **context)
    elif User.current_login_user.role == "student":
        student_obj = User.current_login_user
        context['student_obj'] = student_obj
        return render_template("11student_info.html", **context)
    else:
        return redirect(url_for("index_page.index"))