from flask import render_template, Blueprint
from model.user import User
from model.user_admin import Admin


index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    context = {}
    # check the class variable User.current_login_user
    if User.current_login_user is not None:
        role = User.current_login_user.role
        context['current_user_role'] = role
    # manually register an admin account when open index page
    admin_obj = Admin(username="admin", password="admin")
    # register admin will only run if it knows username admin does not exist in user.txt
    admin_obj.register_admin()
    return render_template("01index.html", **context)



