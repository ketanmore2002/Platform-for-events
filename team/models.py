from http.client import PAYMENT_REQUIRED
from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class host (models.Model):
    user_name = models.CharField(max_length=300,blank=True,null=True) 
    user_id = models.CharField(max_length=300,blank=True,null=True) 
    user_email = models.CharField(max_length=300,blank=True,null=True)
    status = models.CharField(max_length=300,blank=True,null=True)


    def __str__(self):
        return str(self.user_name)
    



class events(models.Model):

    host_name = models.CharField(max_length=300,blank=True,null=True) 
    host_user_name = models.CharField(max_length=300,blank=True,null=True)
    host_user_id = models.CharField(max_length=300,blank=True,null=True)
    host_email = models.CharField(max_length=300,blank=True,null=True)
    host_phone = models.CharField(max_length=300,blank=True,null=True)
    event_name = models.CharField(max_length=300,blank=True,null=True)
    opening_event_date = models.CharField(max_length=300,blank=True,null=True)
    closing_event_date = models.CharField(max_length=300,blank=True,null=True)
    event_date = models.CharField(max_length=300,blank=True,null=True)
    event_venue = models.CharField(max_length=1000,blank=True,null=True)
    number_of_members_allowed = models.CharField(max_length=300,blank=True,null=True, default="1") #team
    # total_number_of_members_allowed = models.CharField(max_length=300,blank=True,null=True, default="1") 
    type_of_event = models.CharField(max_length=30,blank=True,null=True) 
    rules = models.TextField(blank=True,null=True)
    discription = models.TextField(blank=True,null=True) 
    event_fee = models.CharField(max_length=30,blank=True,null=True)
    poster_url = models.CharField(max_length=300,blank=True,null=True)
    first_prize = models.CharField(max_length=300,blank=True,null=True)
    second_prize = models.CharField(max_length=300,blank=True,null=True)
    third_prize = models.CharField(max_length=300,blank=True,null=True)
    current_members_in_event = models.IntegerField(blank=True,null=True, default=0) #current
    number_of_members_allowed_in_event = models.IntegerField(blank=True,null=True, default=0)#event
    entry = models.CharField(max_length=300,blank=True,null=True, default="1")
    rank = models.CharField(max_length=300,blank=True,null=True)



    

    # def __str__(self):
    #     return self.event_name


class teams(models.Model):

    team_name = models.CharField(max_length=300,blank=True,null=True)
    number_of_members = models.IntegerField(blank=True,null=True) #team
    name_of_members = models.CharField(max_length=300,blank=True,null=True) 
    event_participated = models.CharField(max_length=300,blank=True,null=True)
    leader = models.CharField(max_length=300,blank=True,null=True) 
    leader_user_name = models.CharField(max_length=300,blank=True,null=True) 
    leader_phone_number = models.CharField(max_length=300,blank=True,null=True) 
    leader_user_id = models.CharField(max_length=300,blank=True,null=True) 
    leader_email = models.CharField(max_length=300,blank=True,null=True)
    event_id = models.CharField(max_length=300,blank=True,null=True)
    college_name = models.CharField(max_length=300,blank=True,null=True)
    payment_status = models.CharField(max_length=30,blank=True,null=True,default="unpaid")


    def __str__(self):
        return self.team_name


class player (models.Model):
    player_name = models.CharField(max_length=300,blank=True,null=True)
    player_user_name = models.CharField(max_length=300,blank=True,null=True) 
    player_user_id = models.CharField(max_length=300,blank=True,null=True) 
    player_email = models.CharField(max_length=300,blank=True,null=True)
    player_phone_number = models.CharField(max_length=300,blank=True,null=True) 
    event_participated = models.CharField(max_length=300,blank=True,null=True)
    event_id = models.CharField(max_length=300,blank=True,null=True)
    college_name = models.CharField(max_length=300,blank=True,null=True)
    payment_status = models.CharField(max_length=30,blank=True,null=True,default="unpaid")




    def __str__(self):
        return self.player_name



