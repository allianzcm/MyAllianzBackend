from django.contrib.auth.models import  BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None):

        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")
        if not first_name:
            raise ValueError("User must have a first name.")
        if not last_name:
            raise ValueError("User must have a last name.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name = first_name,
            last_name = last_name,
      )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name,password,gender,phone):

        user = self.create_user(
           email=self.normalize_email(email),
           username=username,
           first_name = first_name,
           last_name = last_name,
           password=password
      )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

