import csv
import os
from datetime import datetime

# File paths for storing records
SUBJECTS_FILE = 'Subjects.csv'
ASSIGNMENTS_FILE = 'Assignments.csv'
GRADES_FILE = 'Grades.csv'


def setup_files():
    # Create empty files with headers if they don't exist
    if not os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject_Name', 'Credits', 'Classes_Held', 'Classes_Attended'])

    if not os.path.exists(ASSIGNMENTS_FILE):
        with open(ASSIGNMENTS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject_Name', 'Assignment_Name', 'Deadline', 'Status'])

    if not os.path.exists(GRADES_FILE):
        with open(GRADES_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject_Name', 'Exam_Name', 'Marks_Secured', 'Max_Marks'])


def read_csv_rows(filename):
    # Reads rows skipping the first header row and empty rows
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = []
        is_header = True
        for row in reader:
            if not row or not any(field.strip() for field in row):
                continue
            if is_header:
                is_header = False
                continue
            rows.append(row)
        return rows


def write_csv_rows(filename, header, rows):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def get_all_subject_names():
    rows = read_csv_rows(SUBJECTS_FILE)
    return [row[0] for row in rows]


# ---------------- ATTENDANCE FUNCTIONS ---------------- #

def add_new_subject():
    print("\n--- Add Subject ---")
    sub_name = input("Enter Subject Name: ").strip()
    if not sub_name:
        print("Subject name cannot be empty.")
        return

    existing = [s.lower() for s in get_all_subject_names()]
    if sub_name.lower() in existing:
        print(f"'{sub_name}' already exists.")
        return

    try:
        credits = int(input("Enter Credits (e.g. 3 or 4): ").strip())
        if credits <= 0:
            print("Credits must be greater than 0.")
            return
    except ValueError:
        print("Please enter a valid integer for credits.")
        return

    with open(SUBJECTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([sub_name, credits, 0, 0])

    print(f"Added {sub_name} ({credits} credits).")


def update_attendance():
    subjects = read_csv_rows(SUBJECTS_FILE)
    if not subjects:
        print("\nNo subjects found. Please add a subject first.")
        return

    print("\nSelect Subject:")
    for idx, row in enumerate(subjects, 1):
        print(f"{idx}. {row[0]} (Current: {row[3]}/{row[2]})")

    try:
        choice = int(input(f"Choice (1-{len(subjects)}): ").strip())
        if not (1 <= choice <= len(subjects)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    selected = subjects[choice - 1]
    held = int(selected[2])
    attended = int(selected[3])

    print("\n1. Attended class")
    print("2. Missed / Bunked class")
    action = input("Enter choice (1 or 2): ").strip()

    if action == '1':
        held += 1
        attended += 1
        print(f"Updated: Attended {selected[0]}.")
    elif action == '2':
        held += 1
        print(f"Updated: Missed {selected[0]}.")
    else:
        print("Invalid choice. Nothing updated.")
        return

    selected[2] = str(held)
    selected[3] = str(attended)
    write_csv_rows(SUBJECTS_FILE, ['Subject_Name', 'Credits', 'Classes_Held', 'Classes_Attended'], subjects)


def calculate_bunk_allowance(held, attended):
    # Simulation approach: test class-by-class instead of single-step algebra
    if held == 0:
        return 0, 0.0, "No classes held yet"

    pct = (attended / held) * 100.0

    if pct >= 75.0:
        # Keep incrementing hypothetical missed classes until attendance drops below 75%
        bunks = 0
        temp_held = held
        while (attended / (temp_held + 1)) * 100.0 >= 75.0:
            bunks += 1
            temp_held += 1

        if bunks > 0:
            status = f"Can safely bunk {bunks} class(es)"
        else:
            status = "At 75% threshold (cannot bunk next class)"
        return bunks, pct, status
    else:
        # Keep incrementing attended classes until attendance hits or passes 75%
        needed = 0
        temp_held = held
        temp_attended = attended
        while (temp_attended / temp_held) * 100.0 < 75.0:
            needed += 1
            temp_held += 1
            temp_attended += 1

        return -needed, pct, f"Must attend next {needed} class(es)"


def show_attendance_report():
    subjects = read_csv_rows(SUBJECTS_FILE)
    if not subjects:
        print("\nNo subjects found.")
        return

    print("\n" + "-" * 75)
    print(f"{'Subject':<22} | {'Held':<6} | {'Attended':<8} | {'Attendance':<10} | {'Status'}")
    print("-" * 75)

    for row in subjects:
        sub_name = row[0]
        held = int(row[2])
        attended = int(row[3])
        _, pct, status = calculate_bunk_allowance(held, attended)
        pct_str = f"{pct:.1f}%" if held > 0 else "N/A"
        print(f"{sub_name:<22} | {held:<6} | {attended:<8} | {pct_str:<10} | {status}")

    print("-" * 75)


# ---------------- ASSIGNMENT FUNCTIONS ---------------- #

def add_assignment():
    subjects = get_all_subject_names()
    if not subjects:
        print("\nPlease add at least one subject first.")
        return

    print("\nSelect Subject:")
    for idx, s in enumerate(subjects, 1):
        print(f"{idx}. {s}")

    try:
        choice = int(input(f"Choice (1-{len(subjects)}): ").strip())
        if not (1 <= choice <= len(subjects)):
            print("Invalid choice.")
            return
        subject_name = subjects[choice - 1]
    except ValueError:
        print("Invalid number.")
        return

    task_name = input("Assignment Title: ").strip()
    if not task_name:
        print("Title cannot be empty.")
        return

    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("Invalid format. Please use YYYY-MM-DD.")
        return

    with open(ASSIGNMENTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([subject_name, task_name, deadline, 'Pending'])

    print(f"Logged task '{task_name}' for {subject_name}.")


def check_off_assignment():
    assignments = read_csv_rows(ASSIGNMENTS_FILE)
    pending = [(idx, row) for idx, row in enumerate(assignments) if row[3].strip().lower() == 'pending']

    if not pending:
        print("\nNo pending assignments found.")
        return

    print("\nPending Assignments:")
    for display_idx, (real_idx, row) in enumerate(pending, 1):
        print(f"{display_idx}. [{row[0]}] {row[1]} (Due: {row[2]})")

    try:
        choice = int(input(f"Select completed assignment (1-{len(pending)}): ").strip())
        if not (1 <= choice <= len(pending)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    target_idx = pending[choice - 1][0]
    assignments[target_idx][3] = 'Completed'

    write_csv_rows(ASSIGNMENTS_FILE, ['Subject_Name', 'Assignment_Name', 'Deadline', 'Status'], assignments)
    print(f"Marked '{assignments[target_idx][1]}' as Completed.")


def show_whats_due_soon():
    assignments = read_csv_rows(ASSIGNMENTS_FILE)
    pending = [row for row in assignments if row[3].strip().lower() == 'pending']

    if not pending:
        print("\nNo pending assignments right now.")
        return

    def parse_deadline(row):
        try:
            return datetime.strptime(row[2], "%Y-%m-%d")
        except ValueError:
            return datetime.max

    pending.sort(key=parse_deadline)

    print("\n" + "-" * 65)
    print(f"{'Subject':<20} | {'Task':<26} | {'Deadline':<12}")
    print("-" * 65)
    for row in pending:
        print(f"{row[0]:<20} | {row[1]:<26} | {row[2]:<12}")
    print("-" * 65)


# ---------------- GRADES & GPA FUNCTIONS ---------------- #

def log_test_score():
    subjects = get_all_subject_names()
    if not subjects:
        print("\nPlease add at least one subject first.")
        return

    print("\nSelect Subject:")
    for idx, s in enumerate(subjects, 1):
        print(f"{idx}. {s}")

    try:
        choice = int(input(f"Choice (1-{len(subjects)}): ").strip())
        if not (1 <= choice <= len(subjects)):
            print("Invalid choice.")
            return
        subject_name = subjects[choice - 1]
    except ValueError:
        print("Invalid number.")
        return

    exam_name = input("Exam / Quiz Name: ").strip()
    if not exam_name:
        print("Name cannot be empty.")
        return

    try:
        scored = float(input("Marks Secured: ").strip())
        total = float(input("Total Marks: ").strip())
        if total <= 0 or scored < 0 or scored > total:
            print("Marks must be between 0 and Total Marks.")
            return
    except ValueError:
        print("Invalid numeric marks entered.")
        return

    with open(GRADES_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([subject_name, exam_name, scored, total])

    print(f"Recorded {scored}/{total} for {exam_name} in {subject_name}.")


def show_all_grades():
    grades = read_csv_rows(GRADES_FILE)
    if not grades:
        print("\nNo test scores logged yet.")
        return

    # Group scores by subject
    grouped = {}
    for row in grades:
        sub, exam, scored, total = row[0], row[1], float(row[2]), float(row[3])
        if sub not in grouped:
            grouped[sub] = []
        grouped[sub].append((exam, scored, total))

    print("\n--- ALL RECORDED TEST SCORES ---")
    for sub, tests in grouped.items():
        print(f"\n{sub}:")
        for exam, scored, total in tests:
            pct = (scored / total) * 100.0
            print(f"  - {exam}: {scored}/{total} ({pct:.1f}%)")


def calculate_gpa_stats():
    subjects = read_csv_rows(SUBJECTS_FILE)
    grades = read_csv_rows(GRADES_FILE)
    if not subjects or not grades:
        return None

    # Calculate aggregate marks scored per subject
    sub_scores = {}
    for row in grades:
        sub = row[0]
        scored = float(row[2])
        total = float(row[3])
        if sub not in sub_scores:
            sub_scores[sub] = [0.0, 0.0]
        sub_scores[sub][0] += scored
        sub_scores[sub][1] += total

    total_weighted_points = 0.0
    evaluated_credits = 0

    for row in subjects:
        sub = row[0]
        credits = int(row[1])
        if sub in sub_scores and sub_scores[sub][1] > 0:
            percentage = (sub_scores[sub][0] / sub_scores[sub][1]) * 100.0
            grade_point = min(10.0, max(0.0, percentage / 10.0))
            total_weighted_points += (grade_point * credits)
            evaluated_credits += credits

    if evaluated_credits == 0:
        return None

    return total_weighted_points / evaluated_credits, evaluated_credits


def guess_my_gpa():
    stats = calculate_gpa_stats()
    if stats is None:
        print("\nNot enough grade data logged to estimate GPA.")
        return

    gpa, total_cr = stats
    print("\n--- ESTIMATED SEMESTER GPA ---")
    print(f"Total Evaluated Credits : {total_cr}")
    print(f"Estimated GPA (10-scale): {gpa:.2f} / 10.00")


# ---------------- DASHBOARD & DEEP DIVE ---------------- #

def subject_deep_dive():
    subjects = read_csv_rows(SUBJECTS_FILE)
    if not subjects:
        print("\nNo subjects found.")
        return

    print("\nSelect Subject:")
    for idx, s in enumerate(subjects, 1):
        print(f"{idx}. {s[0]}")

    try:
        choice = int(input(f"Choice (1-{len(subjects)}): ").strip())
        if not (1 <= choice <= len(subjects)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    selected = subjects[choice - 1]
    sub_name = selected[0]
    credits = selected[1]
    held = int(selected[2])
    attended = int(selected[3])

    print("\n" + "=" * 50)
    print(f"SUMMARY: {sub_name.upper()} ({credits} Credits)")
    print("=" * 50)

    # Attendance
    _, pct, status = calculate_bunk_allowance(held, attended)
    pct_str = f"{pct:.1f}%" if held > 0 else "N/A"
    print(f"\nAttendance : {attended}/{held} ({pct_str})")
    print(f"Status     : {status}")

    # Assignments
    assignments = read_csv_rows(ASSIGNMENTS_FILE)
    sub_tasks = [r for r in assignments if r[0].lower() == sub_name.lower()]
    print("\nAssignments:")
    if not sub_tasks:
        print("  None logged.")
    else:
        for t in sub_tasks:
            print(f"  - {t[1]} (Due: {t[2]}) [{t[3]}]")

    # Grades
    grades = read_csv_rows(GRADES_FILE)
    sub_grades = [r for r in grades if r[0].lower() == sub_name.lower()]
    print("\nExam Scores:")
    if not sub_grades:
        print("  None logged.")
    else:
        tot_scored, tot_max = 0.0, 0.0
        for g in sub_grades:
            sc, mx = float(g[2]), float(g[3])
            tot_scored += sc
            tot_max += mx
            print(f"  - {g[1]}: {sc:.1f}/{mx:.1f} ({(sc/mx)*100:.1f}%)")
        if tot_max > 0:
            print(f"  Total: {tot_scored:.1f}/{tot_max:.1f} ({(tot_scored/tot_max)*100:.1f}%)")


def show_morning_dashboard():
    subjects = read_csv_rows(SUBJECTS_FILE)
    assignments = read_csv_rows(ASSIGNMENTS_FILE)

    print("\n" + "=" * 50)
    print("                MORNING DASHBOARD")
    print("=" * 50)

    # 1. Attendance alerts
    print("\n1. ATTENDANCE ALERTS (< 75%):")
    alert_count = 0
    for row in subjects:
        try:
            held = int(row[2])
            attended = int(row[3])
        except (ValueError, IndexError):
            continue

        if held > 0:
            _, pct, status = calculate_bunk_allowance(held, attended)
            if pct < 75.0:
                alert_count += 1
                print(f"   ! {row[0]}: {pct:.1f}% -> {status}")
    if alert_count == 0:
        print("   All subjects above 75%.")

    # 2. Upcoming tasks
    print("\n2. UPCOMING ASSIGNMENTS:")
    pending = [r for r in assignments if len(r) >= 4 and r[3].strip().lower() == 'pending']

    def parse_deadline(row):
        try:
            return datetime.strptime(row[2], "%Y-%m-%d")
        except ValueError:
            return datetime.max

    pending.sort(key=parse_deadline)
    top_3 = pending[:3]
    if not top_3:
        print("   No pending tasks.")
    else:
        for idx, task in enumerate(top_3, 1):
            print(f"   {idx}. {task[1]} ({task[0]}) - Due: {task[2]}")

    # 3. Estimated GPA
    print("\n3. ESTIMATED GPA:")
    stats = calculate_gpa_stats()
    if stats:
        gpa, _ = stats
        print(f"   Current GPA: {gpa:.2f} / 10.00")
    else:
        print("   No grades logged yet.")
    print("=" * 50)


# ---------------- MAIN APPLICATION LOOP ---------------- #

def print_menu():
    print("\n--- Student Academic Tracker ---")
    print("1.  Morning Dashboard")
    print("2.  Add New Subject")
    print("3.  Log Attendance")
    print("4.  Attendance & Bunk Report")
    print("5.  Add Assignment")
    print("6.  View Pending Deadlines")
    print("7.  Mark Assignment as Completed")
    print("8.  Log Test / Exam Marks")
    print("9.  View All Test Scores")
    print("10. View Estimated GPA")
    print("11. Subject Deep Dive")
    print("0.  Exit")


def main():
    setup_files()

    while True:
        print_menu()
        choice = input("Enter choice (0-11): ").strip()

        if choice == '1':
            show_morning_dashboard()
        elif choice == '2':
            add_new_subject()
        elif choice == '3':
            update_attendance()
        elif choice == '4':
            show_attendance_report()
        elif choice == '5':
            add_assignment()
        elif choice == '6':
            show_whats_due_soon()
        elif choice == '7':
            check_off_assignment()
        elif choice == '8':
            log_test_score()
        elif choice == '9':
            show_all_grades()
        elif choice == '10':
            guess_my_gpa()
        elif choice == '11':
            subject_deep_dive()
        elif choice == '0':
            print("\nExiting. Records saved.\n")
            break
        else:
            print("Invalid choice. Please select 0 to 11.")


if __name__ == "__main__":
    main()