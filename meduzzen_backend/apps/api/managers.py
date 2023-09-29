from django.contrib.auth.models import BaseUserManager

# Custom User model manager for django admin
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, username, first_name, last_name, **extra_fields)