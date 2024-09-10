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


CHARGE_TYPE = (
    ("Hourly",  'Hourly'),
    ("Day Charge", 'Day Charge'),
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
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture_new/', blank=True, default='images/profile.png')
    about = models.TextField(max_length=10000, blank=True, null=True)
    category = models.ManyToManyField('siyyana_app.Category',blank=True)
    subcategory = models.ManyToManyField('siyyana_app.SubCategory',blank=True,related_name='subcategory')
    charge = models.CharField(max_length=20, blank=True, null=True, choices=CHARGE_TYPE)
    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    is_active = models.CharField(max_length=20,null=True,blank=True, default="Active")
    user_type = models.CharField(max_length=20,null=True,blank=True,choices=USER_TYPE)
    fcm_token = models.CharField(max_length=1000, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    approval_status = models.CharField(max_length=20, blank=True, null=True, choices=APPROVAL_CHOICES, default="Pending")
    country = models.ForeignKey('siyyana_app.Country', on_delete=models.SET_NULL, null=True, blank=True,related_name='customuser_country')
    state = models.ForeignKey('siyyana_app.State', on_delete=models.SET_NULL, null=True, blank=True,related_name='customuser_state')
    district = models.ForeignKey('siyyana_app.District', on_delete=models.SET_NULL, null=True, blank=True,related_name='customuser_district')
    prefered_work_location = models.ForeignKey('siyyana_app.District', on_delete=models.SET_NULL, null=True, blank=True,related_name='customuser_prefered_work_location')
    id_card_type = models.CharField(max_length=20, blank=True, null=True)
    id_card_number = models.CharField(max_length=20, blank=True, null=True)
    id_card = models.FileField(upload_to='id_card/', blank=True, null=True)
    # OTP fields for forgot password functionality
    otp = models.CharField(max_length=6, blank=True, null=True)  # Store OTP
    otp_created_at = models.DateTimeField(blank=True, null=True)  # Store OTP creation time

    def __str__(self):
        return  f'{str(self.name)} - {str(self.user_type)}'
    







class EmployeeWorkSchedule(models.Model):
    class Meta:
        verbose_name_plural = "EMPLOYEE WORK SCHEDULE"
    def __str__(self):
        return f"Un: {self.user} - Mob: {self.user.mobile_number} - Type: {self.user.user_type} "
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True,related_name='employee_work_schedule')
    sunday_start_time = models.TimeField(blank=True, null=True)
    sunday_end_time = models.TimeField(blank=True, null=True)
    monday_start_time = models.TimeField(blank=True, null=True)
    monday_end_time = models.TimeField(blank=True, null=True)
    tuesday_start_time = models.TimeField(blank=True, null=True)
    tuesday_end_time = models.TimeField(blank=True,null=True)
    wednesday_start_time = models.TimeField(blank=True,null=True)
    wednesday_end_time = models.TimeField(blank=True,null=True)
    thursday_start_time = models.TimeField(blank=True,null=True)
    thursday_end_time = models.TimeField(blank=True,null=True)
    friday_start_time = models.TimeField(blank=True,null=True)
    friday_end_time = models.TimeField(blank=True,null=True)
    saturday_start_time = models.TimeField(blank=True,null=True)
    saturday_end_time = models.TimeField(blank=True,null=True)



class EmployyeWages(models.Model):
    class Meta:
        verbose_name_plural = "EMPLOYEE WAGES"
    def __str__(self):
        return f"Un: {self.user} - Mob: {self.user.mobile_number} - Type: {self.user.user_type} "
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True,related_name='employee_wages')
    subcategory = models.ForeignKey('siyyana_app.SubCategory', on_delete=models.CASCADE,blank=True,null=True)
    wages = models.IntegerField(blank=True,null=True)
