"""
Welcome to the HospiCheck application.
This program facilitates medical application for small clinics like a barangay
clinic. The aim for this program is to digitize analog medical applications for
better process.

Suggestions:
1. Add the availability of the doctor (via a predetermined schedule)
2. To prevent an immediate re-schedule/addition/cancellation, there should be
   a firewall/border
3. Add an option to clear appointments based on the dates to free up space and/or urgency
"""

import csv
import heapq
from collections import defaultdict

# Data structures
appointments = []  # Priority queue
appointments_by_date = defaultdict(int)  # Count of appointments per day
patient_records = {}  # Hash table for patients

CSV_FILE = "appointments.csv"

# Load appointments from CSV
def load_appointments():
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patient_id = row['patient_id']
                if patient_id in patient_records:
                    continue  # Skip if already loaded

                urgency = int(row['urgency'])
                name = row['patient_name']
                date = row['date']

                heapq.heappush(appointments, (urgency, patient_id, name, date))
                appointments_by_date[date] += 1
                patient_records[patient_id] = (name, date, urgency)
    except FileNotFoundError:
        pass


# Save appointments to CSV
def save_appointments():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['urgency', 'patient_id', 'patient_name', 'date'])
        for urgency, patient_id, name, date in appointments:
            writer.writerow([urgency, patient_id, name, date])

# Display help

def show_help():
    print("""How to use HospiCheck:
    1. You can book, reschedule, or cancel appointments on Current Appointment List.
    2. When booking, fill up the following forms: patient ID (use default numbering (e.g., 01, 02) if no ID is
       presented), patient name, urgency (0 for emergency; 1 for routine), and the date of appointment.
    3. Only a maximum of 5 appointments are allowed per day in this system. Free up some space if they've
       arrived or canceled their appointment
        """)
    go_back = input("If you understood all, enter 1 to return to menu: ")  # returns to the main menu
    if go_back == '1':
        return main()

# Display appointment list

def display_appointments():
    if not appointments: # translation: if there is/are no appointments
        print("There are no appointments. Would you like to add? Enter 1 for yes, 0 for no")
        return input("Choice: ") == '1'
    print("Current Appointments:")
    for urgency, patient_id, name, date in appointments:
        print(f"{name} (ID: {patient_id}) - Date: {date}, Urgency: {'Emergency' if urgency == 0 else 'Routine'}")
    return handle_existing_appointments()

# Handle existing appointments menu

def handle_existing_appointments():
    print("\nWould you like to reschedule, add more, or cancel an appointment?")
    print("""Enter 0 to Reschedule
Enter 1 to Add another
Enter 2 to Cancel
Enter 3 to return to main menu""")
    choice = input("Choice: ")
    if choice == '0':
        reschedule_appointment()
    elif choice == '1':
        book_appointment()
    elif choice == '2':
        cancel_appointment()
    return False

# Book appointment

def book_appointment():
    print("Book an Appointment")
    patient_id = input("Enter Patient ID: ")
    name = input("Enter Patient Name: ")
    urgency = int(input("Enter Urgency (0 for Emergency, 1 for Routine): "))

    # Suggest the earliest available day for routine
    date = input("Enter Appointment Date: ")
    if urgency == 1:
        for offset in range(30):
            proposed_date = date  # Replace with proper date arithmetic if desired
            if appointments_by_date[proposed_date] < 5:
                date = proposed_date
                break

    if appointments_by_date[date] >= 5:
        print("Date full. Cannot book.")
        return

    heapq.heappush(appointments, (urgency, patient_id, name, date))
    appointments_by_date[date] += 1
    patient_records[patient_id] = (name, date, urgency)
    save_appointments()
    print("Appointment booked.")

# Method reschedule_appointment reschedules an existing appointment

def reschedule_appointment():
    print("""----------------------------------------------
Reschedule an Appointment""")
    patient_id = input("Enter Patient ID to reschedule: ")
    if patient_id not in patient_records:
        print("Patient not found.")
        return

    # Get current details
    name, old_date, urgency = patient_records[patient_id]

    # Remove old appointment
    appointments[:] = [appt for appt in appointments if appt[1] != patient_id]
    heapq.heapify(appointments)
    appointments_by_date[old_date] -= 1
    del patient_records[patient_id]
    save_appointments()

    # Ask only for new date
    print(f"Rescheduling for {name} (ID: {patient_id}), current urgency: {'Emergency' if urgency == 0 else 'Routine'}")
    new_date = input("Enter new Appointment Date: ")

    if urgency == 1:
        for offset in range(30):
            proposed_date = new_date  # Optionally apply date shifting
            if appointments_by_date[proposed_date] < 5:
                new_date = proposed_date
                break

    if appointments_by_date[new_date] >= 5:
        print("Date full. Cannot reschedule.")
        return

    # Inserts the new rescheduled appointment
    heapq.heappush(appointments, (urgency, patient_id, name, new_date))
    appointments_by_date[new_date] += 1
    patient_records[patient_id] = (name, new_date, urgency)
    save_appointments()
    print("Appointment rescheduled.")


# Cancel appointment

def cancel_appointment():
    print("""----------------------------------------------
Cancel an Appointment""")
    patient_id = input("Enter Patient ID to cancel: ")
    if patient_id not in patient_records:
        print("Patient not found. Try again")
        return
    date = patient_records[patient_id][1]
    appointments[:] = [appt for appt in appointments if appt[1] != patient_id]
    heapq.heapify(appointments)
    del patient_records[patient_id]
    appointments_by_date[date] -= 1
    save_appointments()
    print("Appointment canceled.")

# Main interface / overall program execution

def main():
    load_appointments()
    while True:
        print("""----------------------------------------------------------------------------------------        
Welcome to HospiCheck! Your trusted clinic appointment application made by IDLE Checkers
Enter 0 for Help
Enter 1 for Current Appointment List
Enter 2 to Exit""")
        choice = input("Choice: ")
        if choice == '0':
            print("---------------------------------------------------------------------------------------")
            show_help()
        elif choice == '1':
            print("---------------------------------------------------------------------------------------")
            if display_appointments():
                print("---------------------------------------------------------------------------------------")
                book_appointment()
        elif choice == '2':
            print("""--------------------------------------------------------------------------------------          
Thank you for using HospiCheck. HospiCheck is made by IDLE Checkers
and the following names are the members:
Navor, Raiven Christian
Nera, Christian Jacob
Ordoño, Jims Harold

This is a mini-project from LORMA Colleges. Have a great day from IDLE Checkers!""")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == '__main__':
    main()