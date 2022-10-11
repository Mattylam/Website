from model.user import User
import re
import os
import random
import math

class Admin(User):
    """
        Admin class inherits from the User class.
        Class Admin creates the basic template for admin

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

        register_admin()
        This method checks the user_admin.txt file to find out whether the username already
        exists or not. If not, register this admin. If it exists, do nothing.

        """
    def __init__(self, uid=-1, username="", password=" ", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="admin"):
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
        self.role = role

    def register_admin(self):
        user_id = super().generate_unique_user_id()
        username = self.username
        password = super().encrypt_password(self.password)
        if super().check_username_exist(username) is False:
            register = str(user_id) + ";;;" + username + ";;;" + password + ";;;" + self.register_time + ";;;" + \
                       self.role
            with open('data/user.txt', 'a') as file:
                file.write("\n" + register)

    def __str__(self):
        super().__str__()
