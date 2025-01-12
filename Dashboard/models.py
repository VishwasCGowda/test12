from django.db import models
from datetime import datetime

class Appointment(models.Model):
    email = models.EmailField(max_length=255)
    hospital_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    consultation_day = models.DateField()
    appointment_date = models.DateTimeField(default=datetime.now)
    consultation_id = models.CharField(max_length=50)
    def __str__(self):
        return f"Appointment with {self.doctor_name} on {self.appointment_date}"


class Consultation(models.Model):
    appointment_id = models.CharField(max_length=50)  # Use ForeignKey for relationships
    doctor_name = models.CharField(max_length=50)
    last_visit = models.DateTimeField(default=datetime.now)
    consultation_notes = models.TextField()
    prescription_text = models.TextField()

    def __str__(self):
        return f"Consultation notes for {self.appointment_id} on {self.last_visit}"
