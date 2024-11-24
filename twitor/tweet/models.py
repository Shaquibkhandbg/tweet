from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/',blank=True,null=True)
    
    #auto_now_add: Sets the timestamp when the object is created. It cannot be updated.
    created_at = models.DateTimeField(auto_now_add=True) 
    
    #Updates the timestamp whenever the object is saved or edited.
    updated_at = models.DateTimeField(auto_now=True) 
    
    
    def __str__(self):
       return f"{self.user.username} - {self.text[:10]}"




# Yes! The fields ID and User_ID are automatically created by Django in the database.

# id : Automatically created by Django for every model, Acts as the primary key, This field is an auto-incrementing integer that uniquely identifies each row in the table.


# user_id: Created due to the ForeignKey relationship, Links to the id