"""
Made a table called user which stores all types of user details.
with following Fields--
first_name-
last_name-
username-
email-
role-
password-
created_date-

"""

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class Users(AbstractUser):
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    username = models.CharField(max_length=100,null=False,unique=True)
    email = models.EmailField(max_length=200,null=False)
    Roles_choice = [("Admin","Admin"),
             ("Student","Student"),
             ("Faculty","Faculty"),]
    Department_choice=  choices=[
                    ('MCA', 'MCA'),
                    ('BCA', 'BCA'),
                    ('BSc CS', 'BSc CS'),
                    ('MSc DS', 'MSc Data Science'),
                ]
    department = models.CharField(choices=Department_choice,null=False)
    role = models.CharField(choices=Roles_choice,default='Student',null=False)
    password = models.CharField(max_length=100,null=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_demo = models.BooleanField(default=False)
    def __str__(self):
        """

        :return: this method help to store data by user's username and role
         instead of the default object name.
        """
        return f"{self.username} {self.role}"
    def is_admin(self):
        return self.role == "Admin"
    def is_faculty(self):
        return self.role == "Faculty"
    def is_student(self):
        return self.role == "Student"
    class Meta:
        """
        changes the database name to user in all small later because SQL has
        problem calling Capital later naming convention.
        """
        db_table = "users"


