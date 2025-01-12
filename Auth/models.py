from django.db import models

class Register(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=256)  # Store encrypted passwords
    role = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

