from django import forms
from django.contrib.auth.models import User
from .models import Patient, MedicalRecord, Doctor, MedicalReports, Medication
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'doctor', 'blood_type', 'age', 'allergies']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment']
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'contact_info']

class MedicalReportsForm(forms.ModelForm):
    class Meta:
        model = MedicalReports
        fields = ['report_file','Test_Name']
        

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30) 
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('doctor', 'I am a Doctor'), ('patient', 'I am a Patient')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        # Exclude fields that are set automatically or shouldn't be edited here
        exclude = ['user', 'slug', 'name']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        # Exclude fields that are set automatically or shouldn't be edited here
        exclude = ['user', 'slug', 'name']

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medicine_name', 'dosage','prescribed_by','dosage','instructions']
   