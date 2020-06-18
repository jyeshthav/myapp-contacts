from django.db import models

# Create your models here.
class Contact(models.Model):
    
    class Meta:
        unique_together = (('name', 'number'),)
        verbose_name_plural = "Contacts"

    name = models.CharField(max_length=150)
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
        