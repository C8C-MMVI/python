import csv
import heapq
from collections import defaultdict

# Data structures
appointments = []  # Priority queue
appointments_by_date = defaultdict(int)  # Count of appointments per day
patient_records = {}  # Hash table for patients
doctor_schedule = defaultdict(list)  # Schedule for doctors by (doctor, date)

CSV_FILE = "appointment.csv"
SCHEDULE_FILE = "schedule.csv"

# Counter for patient ID
global_patient_counter = {
    'priority': 1,
    'regular': 1
}

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

                    priority = int(row['priority'])
                    name = row['patient_name']
                    date = row['date']
                    time = row['time']
                    age = row['age']
                    gender = row['gender']
                    program = row['program']

                    heapq.heappush(appointments, (priority, patient_id, name, date, time, age, gender, program))
                    appointments_by_date[date] += 1
                    patient_records[patient_id] = (name, date, time, priority, age, gender, program)
                except (ValueError, KeyError) as e:
                    print(f"Skipping corrupted row {row}: {e}")
    except FileNotFoundError:
        pass

# Save appointments to CSV
def save_appointments():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['priority', 'patient_id', 'patient_name', 'date', 'time', 'age', 'gender', 'program'])
        for priority, patient_id, name, date, time, age, gender, program in appointments:
            writer.writerow([priority, patient_id, name, date, time, age, gender, program])

# Load doctor schedule from CSV
def load_doctor_schedule():
    try:
        with open(SCHEDULE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    doctor_name, date, time_slot = row
                    doctor_schedule[(doctor_name, date)].append(time_slot)
    except FileNotFoundError:
        pass

# Add doctor schedule
def add_doctor_schedule():
    print("Add Doctor Schedule")
    doctor_name = input("Enter Doctor's Name: ").strip()
    no_of_days = int(input("Enter the number of days to schedule: "))

    with open(SCHEDULE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for _ in range(no_of_days):
            date = input("Enter the date (MM-DD): ").strip()
            num_slots = int(input(f"Enter number of time slots for {date}: "))
            for i in range(num_slots):
                start_time = input(f"Enter start of slot {i+1}: ").strip()
                end_time = input("Enter end of slot: ").strip()
                slot = f"{start_time} - {end_time}"
                writer.writerow([doctor_name, date, slot])
                doctor_schedule[(doctor_name, date)].append(slot)
            print(f"Schedule added for Dr. {doctor_name} on {date}.")

# View doctor's schedule
def view_doctor_schedule():
    print("View Doctor Schedule")
    doctor_name = input("Enter Doctor's Name: ").strip()
    date = input("Enter the date to view schedule (MM-DD): ").strip()
    key = (doctor_name, date)
    if key in doctor_schedule:
        print(f"Schedule for Dr. {doctor_name} on {date}:")
        for i, slot in enumerate(doctor_schedule[key], 1):
            print(f"  {i}. {slot}")
        go_back = input("Enter 1 to return to menu: ")  # returns to the main menu
        if go_back == '1':
            return main()
    else:
        print("No schedule available for this doctor on that date.")

# Book appointment
def book_appointment():
    print("Book an Appointment")
    name = input("Enter Patient Name: ")
    age = input("Enter Age: ")
    gender = input("Enter Gender: ")

    age_int = int(age)
    if age_int >= 60:
        print("Age 60 or above detected. Automatically marked as Priority.")
        priority = 0
    else:
        priority = int(input("Enter Priority (0 for Priority, 1 for Regular): "))

    program = input("Enter Program (Dental, Medical, Optical, Others): ")
    date = input("Enter Appointment Date (YYYY-MM-DD): ").strip()

    # Check if date is in schedule
    available_slots = []
    for (doctor, sched_date), slots in doctor_schedule.items():
        if sched_date == date:
            available_slots.extend(slots)

    if not available_slots:
        print("No available doctor schedule for that date. Please choose another date.")
        return

    print("Available Time Slots:")
    for i, slot in enumerate(available_slots, 1):
        print(f"{i}. {slot}")
    chosen = int(input("Choose a time slot: "))
    if not (1 <= chosen <= len(available_slots)):
        print("Invalid slot selected.")
        return
    chosen_slot = available_slots[chosen - 1]

    if appointments_by_date[date] >= 5:
        print("Date full. Cannot book.")
        return

    patient_id = f"{priority + 1}-{global_patient_counter['priority' if priority == 0 else 'regular']:03d}"
    global_patient_counter['priority' if priority == 0 else 'regular'] += 1

    heapq.heappush(appointments, (priority, patient_id, name, date, chosen_slot, age, gender, program))
    appointments_by_date[date] += 1
    patient_records[patient_id] = (name, date, chosen_slot, priority, age, gender, program)
    save_appointments()
    print("Appointment booked successfully!")

# Display help
def show_help():
    print("""How to use MediCheck- Barangay edition:
1. Book, reschedule, or cancel appointments.
2. Each appointment includes: name, age, gender, priority (0 or 1), date, and program.
3. Add doctor schedules first; patients pick from them when booking.
4. Only 5 appointments per day allowed.
""")
    go_back = input("If you understood all, enter 1 to return to menu: ")  # returns to the main menu
    if go_back == '1':
        return main()

# Display current appointments
# Display current appointments
def display_appointments():
    if not appointments:
        print("There are no appointments.")
        choice = input("Would you like to add an appointment? (Enter 1 for Yes, 0 for No): ")
        if choice == '1':
            book_appointment()
        else:
            print("Returning to main menu...")
        return

    print("Current Appointments:")
    for priority, patient_id, name, date, time, age, gender, program in appointments:
        print(f"{name} (ID: {patient_id}) - Date: {date}, Time: {time}, "
              f"Priority: {'Priority' if priority == 0 else 'Regular'}, "
              f"Age: {age}, Gender: {gender}, Program: {program}")

    handle_existing_appointments()


# Handle options after viewing appointments
def handle_existing_appointments():
    print("""\nOptions:
0 - Reschedule
1 - Add another
2 - Cancel
3 - Clear by date
4 - Return to main menu""")
    choice = input("Choice: ")
    if choice == '0':
        reschedule_appointment()
    elif choice == '1':
        book_appointment()
    elif choice == '2':
        cancel_appointment()
    elif choice == '3':
        clear_appointments_by_date()
    return False

# Reschedule appointment
def reschedule_appointment():
    print("Reschedule Appointment")
    patient_id = input("Enter Patient ID: ")
    if patient_id not in patient_records:
        print("Patient not found.")
        return
    name, old_date, old_time, priority, age, gender, program = patient_records[patient_id]

    # Remove the current appointment from the list
    appointments[:] = [appt for appt in appointments if appt[1] != patient_id]
    heapq.heapify(appointments)
    appointments_by_date[old_date] -= 1
    del patient_records[patient_id]

    print(f"Currently scheduled: {name} on {old_date} at {old_time}")

    # Ask for new date
    new_date = input("Enter new date (MM-DD): ").strip()

    # Check for available time slots for the new date
    available_slots = []
    for (doctor, sched_date), slots in doctor_schedule.items():
        if sched_date == new_date:
            available_slots.extend(slots)

    if not available_slots:
        print("No available doctor schedule for that date. Please choose another date.")
        return

    print("Available Time Slots:")
    for i, slot in enumerate(available_slots, 1):
        print(f"{i}. {slot}")
    chosen = int(input("Choose a time slot: "))
    if not (1 <= chosen <= len(available_slots)):
        print("Invalid slot selected.")
        return
    chosen_slot = available_slots[chosen - 1]

    # Rebook the appointment with the new date and time
    heapq.heappush(appointments, (priority, patient_id, name, new_date, chosen_slot, age, gender, program))
    appointments_by_date[new_date] += 1
    patient_records[patient_id] = (name, new_date, chosen_slot, priority, age, gender, program)
    save_appointments()
    print(f"Appointment rescheduled successfully to {new_date} at {chosen_slot}!")


# Cancel appointment
def cancel_appointment():
    print("Cancel Appointment")
    patient_id = input("Enter Patient ID: ")
    if patient_id not in patient_records:
        print("Patient not found.")
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
    print("Clear Appointments by Date")
    target_date = input("Enter date (YYYY-MM-DD): ")
    global appointments
    cleared = [appt for appt in appointments if appt[3] == target_date]
    if not cleared:
        print("No appointments found on that date.")
        return
    appointments = [appt for appt in appointments if appt[3] != target_date]
    heapq.heapify(appointments)
    for _, patient_id, *_ in cleared:
        if patient_id in patient_records:
            del patient_records[patient_id]
    appointments_by_date[target_date] = 0
    save_appointments()
    print(f"Cleared {len(cleared)} appointments.")

# Main interface
def main():
    load_appointments()
    load_doctor_schedule()
    while True:
        print("""----------------------------------------------------------------------------------------
Welcome to MediCheck – Barangay Edition! Your trusted barangay clinic appointment system
brought to you by IDLE Checkers. If you are a new user, we recommend to read the physical
copy of the manual or enter 0 for the digital form. Enter:
    0 for Help
    1 to View Appointments
    2 to Add Doctor Schedule
    3 to View Doctor Schedule
    4 to Exit""")
        choice = input("The menu to choose: ")
        if choice == '0':
            show_help()
        elif choice == '1':
            display_appointments()
        elif choice == '2':
            add_doctor_schedule()
        elif choice == '3':
            view_doctor_schedule()
        elif choice == '4':
            print("""--------------------------------------------------------------------------------------          
Thank you for using MediCheck- Barangay edition. MediCheck- Barangay edition is made by IDLE Checkers
and the following names are the members:
Navor, Raiven Christian
Nera, Christian Jacob
Ordoño, Jims Harold

This is a mini-project from LORMA Colleges. Have a great day from IDLE Checkers!""")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
