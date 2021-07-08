from apps.patient.models import initialize_table_creation


def create_patient_visits():
    """
    This function helps to create multiple visits for a patient.

    Note:- System will not create patient visit if same doctor and appointment is already assigned with patient

    Requirements:-

    Patient - Email ID
    Doctor - Registered email id of Doctor
    Appointment date - Must be (YYYY-MM-DD) format

    """

    email = "damyanti@yopmail.com"  # give patient email here

    # Assign registered doctor email, and similar length of appointment date and prescriptions

    doctor_list = [
        {'doctor': 'amit@apollo.com', 'appointment_date': '2021-06-22', 'prescription': 'EyeSite Blur'},
        {'doctor': 'rustam@lifecare.com', 'appointment_date': '2021-07-02', 'prescription': 'High Cough'},
        {'doctor': 'mitranshi@victoria.com', 'appointment_date': '2021-06-12', 'prescription': 'High Fever'},
        {'doctor': 'kishor@apollo.com', 'appointment_date': '2021-06-18', 'prescription': 'Skin Infections'}
    ]

    initialize_table_creation(email=email, doctor_list=doctor_list)
