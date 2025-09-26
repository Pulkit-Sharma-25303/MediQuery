import io
from django.shortcuts import render, get_object_or_404
from .models import Patient, MedicalRecord, Doctor, MedicalReports, Medication
from .forms import PatientForm, MedicalRecordForm, DoctorForm, MedicalReportsForm, SignUpForm, PatientProfileForm, DoctorProfileForm, MedicationForm
from django.shortcuts import redirect
import ollama
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from PIL import Image
from pdf2image import convert_from_path
import os
import pytesseract
import fitz  # PyMuPDF
def is_doctor(user):
    return user.groups.filter(name='Doctors').exists()

def is_patient(user):
    return user.groups.filter(name='Patients').exists()



def homepage(request):
    return render(request, 'Core/homepage.html')

@login_required
def patient_list(request):
    if is_doctor(request.user):
        # Doctors can see all patients
        patients = Patient.objects.all()
    else:
        # Patients can only see their own profile in the list
        patients = Patient.objects.filter(user=request.user)
        
    return render(request, 'Core/patient_list.html', {'patients': patients})
@login_required
def complete_profile(request):
    if is_doctor(request.user):
        profile = get_object_or_404(Doctor, user=request.user)
        FormClass = DoctorProfileForm
    else: # is_patient
        profile = get_object_or_404(Patient, user=request.user)
        FormClass = PatientProfileForm
        
    if request.method == 'POST':
        form = FormClass(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Home') # Redirect to homepage after completion
    else:
        form = FormClass(instance=profile)
        
    return render(request, 'registration/complete_profile.html', {
        'form': form
    })


@login_required
@user_passes_test(is_doctor)
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Patient List')
    else:
        form = DoctorForm()
    return render(request, 'Core/create_doctor.html', {'form': form})
@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'Core/doctor_list.html', {'doctors': doctors})
@login_required
def doctor_detail(request, slug):
    from .models import Doctor
    doctor = get_object_or_404(Doctor, slug=slug)
    patients = Patient.objects.filter(doctor=doctor)
    return render(request, 'Core/doctor_detail.html', {'doctor': doctor, 'patients': patients})

@login_required
@user_passes_test(is_doctor)
def medication_list(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    if is_patient(request.user) and patient.user != request.user:
        return redirect('Patient List')
    medications = Medication.objects.filter(patient=patient).order_by('-date_prescribed')
    return render(request, 'Core/medication_list.html', {'patient': patient, 'medications': medications})
@login_required
@user_passes_test(is_doctor)
def add_medication(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.patient = patient
            # You might need to adjust this line based on your Doctor model
            medication.prescribed_by = get_object_or_404(Doctor, user=request.user)
            medication.save()
            return redirect('Patient Detail', slug=patient.slug)
    else:
        # This 'else' block handles the initial GET request
        form = MedicationForm()
    
    # This return statement is now outside the 'if' block
    # and will run for GET requests or if the POST form is invalid.
    return render(request, 'Core/add_medication.html', {
        'form': form,
        'patient': patient
    })

@login_required
def patient_detail(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    if is_patient(request.user) and patient.user != request.user:
        return redirect('Patient List')
    records = MedicalRecord.objects.filter(patient=patient).order_by('-date_created')
    reports = MedicalReports.objects.filter(patient=patient).order_by('-date_uploaded')
    medication = Medication.objects.filter(patient=patient).order_by('-date_prescribed')
    ai_response = None # Initialize ai_response to None
    medicine_context = ""
    report_context = ""
    # Handle the AI query form submission
    if request.method == 'POST':
        query = request.POST.get('query', '')
        selected_report_ids = request.POST.getlist('selected_reports')
        selected_reports = reports.filter(report_id__in=selected_report_ids)
        
        # 1. Format the medical records into a single text block
        records_context = f"Patient Name: {patient.name}\nAge: {patient.age}\nAllergies: {patient.allergies}\n\n--- Medical History ---\n"
        for record in records:
            records_context += (
                f"\nDate: {record.date_created.strftime('%Y-%m-%d')}\n"
                f"Diagnosis: {record.diagnosis}\n"
                f"Treatment: {record.treatment}\n"
                f"---------------------\n"
            )
        for medicine in medication:
            medicine_context += (
                f"\nMedication: {medicine.medicine_name}\n"
                f"Dosage: {medicine.dosage}\n"
                f"Prescribed By: {medicine.prescribed_by.name}\n"
                f"Date Prescribed: {medicine.date_prescribed.strftime('%Y-%m-%d')}\n"
                f"---------------------\n"
            )
        for report in selected_reports:
            if report.summary:
                report_context += (
                    f"\nReport Name: {report.Test_Name}\n"
                    f"Date Uploaded: {report.date_uploaded.strftime('%Y-%m-%d')}\n"
                    f"Summary: {report.summary}\n"
                    f"---------------------\n"
                )
        # 2. Build the prompt for the Ollama model
        prompt = (
            f"Based on the following medical records, please answer the user's query.\n\n"
            f"User Query: '{query}'\n\n"
            f"Medical Records:\n{records_context}"
            f"Medicines:\n{medicine_context}"
            f"Reports:\n{report_context}\n\n"
        )

        try:
            # 3. Call the Ollama API
            response = ollama.chat(
                model='mistral:latest', # Or whichever model you are using
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful medical assistant. Analyze the provided medical records to answer questions or provide summaries. Be concise and accurate.',
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ]
            )
            ai_response = response['message']['content']
        
        except Exception as e:
            # Handle cases where Ollama is not running or there's an API error
            ai_response = f"Error: Could not connect to Ollama. Please ensure it is running. Details: {e}"

    # Prepare the context for the template
    context = {
        'patient': patient,
        'records': records,
        'reports': reports,
        'medication': medication,
        'ai_response': ai_response
    }
    
    return render(request, 'Core/patient_detail.html', context)
@login_required
@user_passes_test(is_doctor)
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Patient List')
    else:
        form = PatientForm()
    return render(request, 'Core/create_patient.html', {'form': form})
@login_required
@user_passes_test(is_doctor)
def create_medical_record(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('Patient List', slug=patient.slug)
    else:
        form = MedicalRecordForm()
    return render(request, 'Core/create_medical_record.html', {
        'form': form,
        'patient': patient
    })
@login_required
@user_passes_test(is_doctor)
def upload_medical_report(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    
    if request.method == 'POST':
        form = MedicalReportsForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.save() # Save the report first to get a file path

            try:
                file_path = report.report_file.path
                file_extension = os.path.splitext(file_path)[1].lower()
                
                text = ""

                # This is the simplified logic for PDF text extraction
                if file_extension == '.pdf':
                    doc = fitz.open(file_path)
                    for page in doc:
                        # Directly extract the text from each page
                        text += page.get_text() + "\n"
                    doc.close()
                
                report.extracted_text = text

                # The summarization logic remains the same
                if text.strip():
                    prompt = f"Please provide a concise summary of the following medical report text, keep it very concise and easy to understand and remember to include exact values in it:\n\n---\n{text}\n---"
                    response = ollama.chat(
                        model='mistral:latest',
                        messages=[{'role': 'user', 'content': prompt}]
                    )
                    report.summary = response['message']['content']
                
                report.save(update_fields=['extracted_text', 'summary'])

            except Exception as e:
                print(f"Error processing report {report.report_id}: {e}")
            
            return redirect('Patient Detail', slug=patient.slug)
    else:
        form = MedicalReportsForm()
        
    return render(request, 'Core/upload_medical_report.html', {
        'form': form,
        'patient': patient
    })
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # This logic remains the same
            role = form.cleaned_data['role']
            if role == 'doctor':
                group = Group.objects.get(name='Doctors')
                Doctor.objects.create(user=user, name=f"{user.first_name} {user.last_name}")
            else:
                group = Group.objects.get(name='Patients')
                Patient.objects.create(user=user, name=f"{user.first_name} {user.last_name}")
            
            user.groups.add(group)
            
            login(request, user)
            # REDIRECT TO THE NEW PROFILE COMPLETION PAGE
            return redirect('complete_profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@user_passes_test(is_doctor)
def medication_list(request, slug):
    patient = get_object_or_404(Patient, slug=slug)
    if is_patient(request.user) and patient.user != request.user:
        return redirect('Patient List')
    medications = Medication.objects.filter(patient=patient).order_by('-date_prescribed')
    return render(request, 'Core/medication_list.html', {'patient': patient, 'medications': medications})
