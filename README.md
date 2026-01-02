# Hospital Management System

This repository contains a simple, role-based Hospital Management System built with Streamlit and PostgreSQL. The application demonstrates secure user authentication, role-specific dashboards, patient data management, and data anonymization.

## Features

- **Secure User Authentication:** Users log in with a username and password. Passwords are securely hashed before being stored.
- **Role-Based Access Control:** The system supports three distinct user roles with different permissions:
    - **Admin:** Can view all raw patient data, trigger the anonymization of specific patient records, and monitor all system activity through a detailed audit log.
    - **Doctor:** Can view anonymized patient data for analysis or research, ensuring patient privacy is maintained.
    - **Receptionist:** Can register new patients by adding their details to the system.
- **Patient Data Management:**
    - Receptionists can add new patients via a simple form.
    - Admins can view a table of all raw patient records.
- **Data Anonymization:** A core feature where an Admin can anonymize a patient's record by their ID. This replaces their name and contact information with masked data, protecting their identity.
- **Audit Logging:** Every significant action, such as login, logout, viewing data, or adding a patient, is logged with a user ID, role, and timestamp. Admins can view these logs and a chart visualizing activity over time.

## Technology Stack

- **Application Framework:** [Streamlit](https://streamlit.io/)
- **Programming Language:** Python
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Python Libraries:**
    - `psycopg2-binary` for PostgreSQL connection
    - `python-dotenv` for managing environment variables
    - `pandas` for data manipulation and display

## Setup and Installation

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/sherrytelli/hospital-management-system.git
cd hospital-management-system
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage project dependencies.
```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all the required Python packages from `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
The application connects to a PostgreSQL database.

1.  Make sure you have a running PostgreSQL instance.
2.  Create a `.env` file in the root directory of the project.
3.  Add your database connection details to the `.env` file:
    ```env
    DB_HOST=your_db_host
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASS=your_db_password
    DB_PORT=your_db_port
    ```

### 5. Initialize the Database
Run the `database.py` script to create the necessary tables (`users`, `patients`, `logs`) and insert default user accounts.

```bash
python database.py
```

This will print a success message if the tables are created and populated correctly.

### 6. Run the Application
Start the Streamlit application with the following command:
```bash
streamlit run app.py
```
Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

Log in with one of the default user accounts created during database initialization.

| Role         | Username      | Password  |
|--------------|---------------|-----------|
| Admin        | `admin`       | `admin123`|
| Doctor       | `Dr. Bob`     | `doc123`  |
| Receptionist | `Alice_recep` | `rec123`  |

- **Admin:**
    - Log in to view the Admin Dashboard.
    - See the "Raw Patient Data" table.
    - Anonymize a record by entering a `Patient ID` and clicking the button.
    - Navigate to the "Audit Log" page to see a log of all actions and an activity chart.

- **Doctor:**
    - Log in to view the Doctor View.
    - You will only see anonymized patient data.

- **Receptionist:**
    - Log in to access the Receptionist View.
    - Use the "Add New Patient" form to register new patients.

## File Structure

```
.
├── app.py                  # Main application file, handles login, session state, and navigation
├── config.py               # Loads database configuration from .env file
├── database.py             # Handles all database operations (connection, queries, initialization)
├── requirements.txt        # Project dependencies
└── pages/
    ├── 01_Admin_Home.py       # Admin dashboard for viewing raw data and anonymization
    ├── 02_Admin_audit.py      # Admin page for viewing audit logs
    ├── 03_Doctor_Home.py      # Doctor's view for anonymized patient data
    └── 04_Receptionist_Home.py# Receptionist's page for adding new patients
