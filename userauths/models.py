from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#---------------------------
#here we are creating a custom user model from django default user model
#this will help us to inherit all properties of django default custom model with all security gievn by django
class User(AbstractUser):
    email= models.EmailField(unique=True) #email already exsist although, this have purpose 
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)        # *extra field 

    USERNAME_FIELD ="email"        #make email as one of the field for log-in 
    REQUIRED_FIELDS = ['username'] #username not pass here, it will omit the django 

    def __str__(self):
        return self.username 

