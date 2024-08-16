from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission



STATUS_CHOICES = (
    (True,  'Active'),
    (False, 'Inactive'),
)

APPROVAL_CHOICES = (
    ("Approved",  'Approved'),
    ("Rejected", 'Rejected'),
    ("Pending",  'Pending'),
)

USER_TYPE = (
    ("Admin",  'Admin'),
    ("User", 'User'),
    ("Employee",  'Employee'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture_new/', blank=True, default='images/profile.png')
    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    is_active = models.CharField(max_length=20,null=True,blank=True, default="Active")
    user_type = models.CharField(max_length=20,null=True,blank=True,choices=USER_TYPE)
    fcm_token = models.CharField(max_length=1000, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    approval_status = models.CharField(max_length=20, blank=True, null=True, choices=APPROVAL_CHOICES, default="Pending")
    def __str__(self):
        return f"Un: {self.username} - Mob: {self.mobile_number} - Type: {self.user_type} - Coins: {self.coins}"
    