from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


class Person(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.Person.save()

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
