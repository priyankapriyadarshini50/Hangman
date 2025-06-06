from django.contrib.auth.models import BaseUserManager

class GameUserManager(BaseUserManager):
    '''Custom manager class for custom user model- GameUser'''
    def create_user(self, email, password=None, **other_fields):
        '''override for creating a custom user'''

        if email is None:
            raise ValueError("msg: Email is required")

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        '''overrride the super user method for creating a user'''

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        user = self.create_user(email=self.normalize_email(email), 
                                password=password, **other_fields)
        user.save(using=self._db)
        return user
