from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_info = models.TextField()
    slug = models.SlugField(unique=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3)
    age = models.IntegerField(null=True, blank=True)
    allergies = models.TextField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.record_id} for {self.patient.name}"

class MedicalReports(models.Model):
    report_id = models.AutoField(primary_key=True)
    Test_Name = models.CharField(max_length=100, default='N/A')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='medical_reports/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"Report {self.Test_Name} for {self.patient.name}"
    

class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date_prescribed = models.DateTimeField(auto_now_add=True)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    

    def __str__(self):
        return self.medicine_name