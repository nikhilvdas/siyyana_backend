from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "COUNTRIES"
    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "STATE"
    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "DISTRICTS"
    def __str__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='category')
    color = models.CharField(max_length=7,blank=True,null=True)
    class Meta:
        verbose_name_plural = "CATEGORY"
    def __str__(self):
        return self.name



class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "SUBCATEGORY"
    def __str__(self):
        return self.name




class RequestedCategory(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=1000)
    class Meta:
        verbose_name_plural = "REQUESTED CATEGORY"
    def __str__(self):
        return self.name
    


class TopCategory(models.Model):
    class Meta:
        verbose_name_plural = "TOP CATEGORY"
    def __str__(self):
        return self.Category.name
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)




STATUS_CHOICES = (
    
    ('Accept',  'Accept'),
    ('Pending', 'Pending'),
    ('Reject', 'Reject'),
    ('Completed', 'Completed'),

)


class Booking(models.Model):
    employee = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,related_name='employee')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,related_name='user')
    service = models.ForeignKey('accounts.EmployyeWages', on_delete=models.SET_NULL, null=True,related_name='service')
    date = models.DateField()
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        verbose_name_plural = "BOOKING"
    def __str__(self):
        return f'{self.user} - {self.service} - {self.date} - {self.status}'



class Review(models.Model):
    class Meta:
        verbose_name_plural = "REVIEWS"
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='reviews')
    employee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='employee_reviews')  # Employee being reviewed
    timing = models.IntegerField()  # Ratings will be from 1 to 5
    service_quality = models.IntegerField()
    behavior = models.IntegerField()
    service_summary = models.CharField(max_length=200,blank=True, null=True)  # Optional comments from the user
    review = models.TextField(blank=True,null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.employee.name} in Booking {self.booking.id}"


class Saved_Employees(models.Model):
    class Meta:
        verbose_name_plural = "SAVED EMPLOYEES"
    def __str__(self):
        return f'{self.user} - {self.employee}'
    employee = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,related_name='saved_employee')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,related_name='saved_user')





