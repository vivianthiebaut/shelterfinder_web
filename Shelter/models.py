from django.db import models
import re
import operator
from functools import reduce
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Shelter(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.CharField(null=True,max_length=200)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    restrictions = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    special_notes = models.CharField(null=True,max_length=200)
    phone_number = models.CharField(max_length=200)
    curr_capacity = models.IntegerField()

    @classmethod
    def create(cls, name, capacity, restrictions, longitude, latitude, address, special_notes, phone_number):
        shelter = cls()
        shelter.name = name
        shelter.capacity = capacity
        shelter.longitude = longitude
        shelter.latitude = latitude
        shelter.restrictions = restrictions
        shelter.address = address
        shelter.special_notes = special_notes
        shelter.phone_number = phone_number

        regex = re.compile("\d+")
        num_beds = regex.findall(shelter.capacity)
        if num_beds:
            shelter.curr_capacity = reduce(operator.add,map(int, num_beds))
        else:
            shelter.curr_capacity = 0
        return shelter


    def make_reservation(self, bed_demand, user):
        if (bed_demand > self.curr_capacity):
            return False
        else:
            user_reservations = self.reservation_set.filter(user_id__exact=user.id)
            r = None
            if user_reservations:
                r=list(user_reservations)[0]
                r.requested_beds += bed_demand
            else:
                r = Reservation(user=user,shelter=self,requested_beds=bed_demand)
            self.curr_capacity -= bed_demand
            self.save()
            r.save()
            return True


    def cancel_reservation(self, bed_demand, user):
        user_reservations = self.reservation_set.filter(user_id__exact=user.id)
        if user_reservations:
            r = list(user_reservations)[0]
            if bed_demand <= r.requested_beds:
                r.requested_beds -= bed_demand
                r.save()
                self.curr_capacity += bed_demand
                self.save()
                return True
            else:
                return False
        return False


class Reservation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter,on_delete=models.CASCADE)
    requested_beds = models.IntegerField()
    reservation_date = models.DateTimeField(default=timezone.now)



