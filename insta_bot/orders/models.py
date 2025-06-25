from django.db import models

class Order(models.Model):
    SERVICE_CHOICES = [
        ('breakfast', 'Nonushta'),
        ('lunch', 'Tushlik'),
        ('dinner', 'Kechki ovqat'),
        ('birthday', 'Tug‘ilgan kun'),
        ('other', 'Boshqa'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    people_count = models.IntegerField(default=1)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='kutilmoqda')

    def __str__(self):
        return f"{self.name} - {self.service_type}"
