# MediQuery: AI-Powered Electronic Health Record (EHR) System

MediQuery is a full-stack web application designed to centralize patient and doctor information securely. It features a robust, role-based authentication system and integrates a local Large Language Model (Ollama) to provide intelligent analysis of medical data, including automated text extraction and summarization from uploaded PDF reports.

***

## Key Features

- 🛡️ **Role-Based Authentication**: Secure signup and login for two distinct user types—**Doctors** and **Patients**—with strict, permission-based access controls.
- 👤 **Patient \& Doctor Management**: Full **CRUD** (Create, Read, Update, Delete) functionality for managing patient profiles, doctor directories, and detailed medical records.
- 📄 **Automated Report Processing**: Upload PDF-based medical reports. The system automatically extracts the text using **PDFPlumber** and generates an **AI-powered summary**.
- 🤖 **AI-Powered Analysis (Ollama)**: An integrated AI assistant allows doctors to **query a patient’s medical history**—including records, medications, and report summaries—using natural language.
- 🔒 **Secure Data Access**: Patients can only view their own profiles and medical data, while doctors can only access the profiles of patients assigned to them.
- 💊 **Medication Tracking**: Doctors can prescribe and manage a list of medications for each patient, including dosage and instructions.

***

## Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS
- **Database**: PostgreSQL, SQLite (for initial development)
- **AI \& Data Processing**: Ollama, PDFPlumber
- **Tools**: DBeaver, Git, Virtual Environments (pip)

***

## Setup and Installation

### Prerequisites

- Python 3.10+ and pip
- PostgreSQL installed and running
- Ollama installed and running (Download from [ollama.com](https://ollama.com/))


### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/Pulkit-Sharma-25303/MediQuery.git
cd MediQuery
```

2. **Set up a virtual environment and install dependencies**

```bash
python -m venv MediEnv
source MediEnv/bin/activate   # On Windows: MediEnv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the Ollama Model**

```bash
ollama pull llama3
```

4. **Configure the Database**
    - Create a PostgreSQL database and user for the project.
    - In your `settings.py`, update the `DATABASES` dictionary with your PostgreSQL credentials.
    - Update your Django `SECRET_KEY`.
5. **Run Database Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a Superuser**

```bash
python manage.py createsuperuser
```

7. **Set Up User Groups (Crucial Step)**
    - Run the server:

```bash
python manage.py runserver
```

    - Log in to the Django admin panel at `/admin/`.
    - Navigate to **Groups** and create two groups with these exact names:
        - `Doctors`
        - `Patients`
8. **Run the Development Server**

```bash
python manage.py runserver
```

The application will be available at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

***

## Usage Workflow

### Sign Up

- Navigate to the **Sign Up** page and create a new account, selecting either the **Doctor** or **Patient** role.


### Complete Profile

- After signing up, complete your profile with necessary details (age, specialty, etc.).


### Doctors

- Can view all patients in the system.
- Can create new patient profiles.
- Can add medical records, prescribe medications, and upload reports for any patient.
- Can use the **AI analysis tool** on a patient’s detail page.


### Patients

- Can only view their **own profile** and medical data.
- Cannot access other patients' information.

***

## License

This project is licensed under the **MIT License**.


