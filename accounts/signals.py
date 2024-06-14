from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customers
from django.contrib.auth.models import Group



def customer_profile(sender, instance,  created, **kwargs):
    if created:
          group = Group.objects.get(name='employee')
          instance.groups.add(group)
          Customers.objects.create(
                user=instance,
                EmployeeName=instance.username,
                )
          print('Profile Created')
post_save.connect(customer_profile, sender=User)
                