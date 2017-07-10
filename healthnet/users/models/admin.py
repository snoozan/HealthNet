from .models import Person

class Admin(Person):
    position = models.CharField(max_length=100)
