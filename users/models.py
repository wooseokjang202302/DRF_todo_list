from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from users import messages


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(messages.REQUIRED_EMAIL)

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=50, verbose_name='name')

    GENDERS = (('M', 'Man'), ('W', 'Woman'))
    gender = models.CharField(verbose_name='gender',
                              max_length=1, choices=GENDERS)

    age = models.IntegerField(verbose_name='age', null=True)
    introduction = models.TextField(
        max_length=500, verbose_name='introduction')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
