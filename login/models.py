from django.db import models
import re
import bcrypt
from datetime import date

class UserManager(models.Manager):
    def basic_validator(self, postData):
        today = date.today()
        age = postData['birthday']
        errors = {}
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['exists'] = "Email already registered"
        else:
            if len(postData['first_name']) == 0:
                errors['no_first_name'] = "You must provide a first name"
            if len(postData['first_name']) < 3 and len(postData['first_name'])  != 0:
                errors['first_name'] = "First name is not long enough"
            if len(postData['last_name']) == 0:
                errors['no_last_name'] = "You must provide a last name"
            if len(postData['last_name']) < 3 and len(postData['last_name']) != 0:
                errors['last_name'] = "Last name is not long enough"
            if len(postData['email']) == 0:
                errors['no_email'] = "You must provide a email"
            EMAIL = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL.match(postData['email']):
                errors['email'] = "Invalid email"
            if len(postData['password']) == 0:
                errors['no_password'] = "You must provide a password"
            if len(postData['password']) < 8 and len(postData['password']) != 0:
                errors['no_password'] = "Your password must have at least 8 characters"
            if postData['password'] != postData['password_c']:
                errors['password_c'] = "Password no son iguales"
            if postData['birthday'] > str(today):
                errors['birthday'] = 'Birthday must be past!'
            # if age.year() - postData['birthday'].year() < 13:
            #     errors['under_age'] = 'You must be at least 13 years old!'
        return errors

    def encriptar(self, password):
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password

    def login_validator(self, password, user):
        errors = {}
        if len(user) > 0:
            # pw_given = postData['password']
            pw_hash = user[0].password
            if bcrypt.checkpw(password.encode(), pw_hash.encode()) is False:
                errors['wrong_pass'] = "Wrong password"
        else:
            errors['invalid_user'] = "User does not exist"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()