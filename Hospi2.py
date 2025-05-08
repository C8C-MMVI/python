"""
THIS IS A BETA PROGRAM OF HOSPICHECK. FURTHER FIXES ARE NEEDED
AFTER THE PRE-DEFENSE
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
                try:
                    patient_id = row['patient_id']
                    if patient_id in patient_records:
                        continue  # Skip if already loaded

                    urgency = int(row['urgency'])
                    name = row['patient_name']
                    date = row['date']

                    heapq.heappush(appointments, (urgency, patient_id, name, date))
                    appointments_by_date[date] += 1
                    patient_records[patient_id] = (name, date, urgency)
                except (ValueError, KeyError) as e:
                    print(f"Skipping corrupted row {row}: {e}")
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
    go_back = input("If you understood all, enter 1 to return to menu: ")
    if go_back == '1':
        return main()

# Display appointment list
def display_appointments():
    if not appointments:
        print("There are no appointments. Would you like to add? Enter 1 for yes, 0 for no")
        return input("Choice: ") == '1'
    print("Current Appointments:")
    for urgency, patient_id, name, date in appointments:
        print(f"{name} (ID: {patient_id}) - Date: {date}, Urgency: {'Emergency' if urgency == 0 else 'Routine'}")
    return handle_existing_appointments()

# Handle existing appointments menu
def handle_existing_appointments():
    print("\nWould you like to reschedule, add more, cancel an appointment, or clear by date?")
    print("""Enter 0 to Reschedule by Date
Enter 1 to Add another
Enter 2 to Cancel
Enter 3 to Clear appointments by date
Enter 4 to return to main menu""")
    choice = input("Choice: ")
    if choice == '0':
        reschedule_by_date()
    elif choice == '1':
        book_appointment()
    elif choice == '2':
        cancel_appointment()
    elif choice == '3':
        clear_appointments_by_date()
    return False

# Book appointment
def book_appointment():
    print("Book an Appointment")
    patient_id = input("Enter Patient ID: ")
    name = input("Enter Patient Name: ")
    urgency = int(input("Enter Urgency (0 for Emergency, 1 for Routine): "))

    date = input("Enter Appointment Date: ")
    if urgency == 1:
        for offset in range(30):
            proposed_date = date
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

# Reschedule appointments by date
def reschedule_by_date():
    print("""----------------------------------------------
Reschedule Appointments by Date""")
    old_date = input("Enter the date to reschedule: ")
    new_date = input("Enter new Appointment Date: ")

    to_reschedule = [appt for appt in appointments if appt[3] == old_date]
    if not to_reschedule:
        print("No appointments found on that date.")
        return

    if appointments_by_date[new_date] + len(to_reschedule) > 5:
        print("New date would exceed maximum appointments. Cannot reschedule.")
        return

    for appt in to_reschedule:
        urgency, patient_id, name, _ = appt
        appointments.remove(appt)
        heapq.heappush(appointments, (urgency, patient_id, name, new_date))
        patient_records[patient_id] = (name, new_date, urgency)

    appointments_by_date[new_date] += len(to_reschedule)
    appointments_by_date[old_date] = 0
    heapq.heapify(appointments)
    save_appointments()
    print(f"Rescheduled {len(to_reschedule)} appointments from {old_date} to {new_date}.")

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

# Clear appointments by date
def clear_appointments_by_date():
    print("""----------------------------------------------
Clear Appointments by Date""")
    target_date = input("Enter the date to clear: ")
    global appointments
    cleared = [appt for appt in appointments if appt[3] == target_date]
    if not cleared:
        print("No appointments found on that date.")
        return

    appointments = [appt for appt in appointments if appt[3] != target_date]
    heapq.heapify(appointments)

    for _, patient_id, _, _ in cleared:
        if patient_id in patient_records:
            del patient_records[patient_id]
    appointments_by_date[target_date] = 0
    save_appointments()
    print(f"Cleared {len(cleared)} appointments on {target_date}.")

# Main interface
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
