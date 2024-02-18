from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Custom_User(AbstractUser):
    User_type=[
        ('admin','Admin'),('student','Student')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=User_type,max_length=120)
    otp_token = models.CharField(max_length=10, null= True, blank=True)

    def __str__(self):
        return self.display_name

class userProfile(models.Model):
    GENDER=(
        ('male', 'Male'),
        ('female', 'Female'),
    )
    name=models.CharField(max_length=30, null=True)
    gender=models.CharField(choices=GENDER, max_length=20)
    weight=models.FloatField()
    height=models.FloatField()
    age=models.FloatField()
    user=models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    BMR = models.FloatField(null = True)
    profile_pic=models.ImageField(upload_to='media/profile_pic', null=True, blank=True)


    def __str__(self):
        return self.name

    
class itemsall(models.Model):
    TIME=(
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Diner', 'Diner'),
    )
    user=models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    item_name=models.CharField(max_length=20)
    time=models.CharField(choices=TIME, max_length=20, null=True)
    calorie_consumed=models.FloatField(null = True)
    create_at=models.DateField(default=timezone.now, null=True)
    date=models.DateField(default=timezone.now, null=True)

    def __str__(self):
        return self.time
    
class date_input(models.Model):
    date=models.DateTimeField(default=timezone.now, editable=False)
    
