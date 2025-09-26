from django.contrib import admin
from .models import Patient, MedicalRecord, Doctor, MedicalReports, Medication  
# Register your models here.
admin.site.register(Patient)
admin.site.register(MedicalRecord)
admin.site.register(Doctor)
admin.site.register(MedicalReports)
admin.site.register(Medication)