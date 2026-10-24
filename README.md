STUDENT ACADEMIC TRACKER (PYTHON CLI)



SHORT DESCRIPTION:

A command-line Student Academic Tracker built in Python to manage college attendance (with a 75% bunk calculator), assignment deadlines, and credit-weighted semester GPA using CSV file storage.



FEATURES:

1. Morning Dashboard: Shows attendance alerts below 75%, top 3 upcoming assignment deadlines, and current estimated GPA.

2. Attendance & Bunk Tracker: Logs attended or missed classes and calculates how many classes you can safely skip or must attend to stay at 75%.

3. Assignment Tracker: Adds assignments with YYYY-MM-DD deadlines, sorts pending tasks by due date, and marks completed tasks.

4. Grade & GPA Calculator: Logs exam scores and calculates credit-weighted semester GPA on a 10-point scale.

5. Subject Deep Dive: Displays complete attendance, assignments, and test scores for any selected subject.



DATA STRUCTURES AND ALGORITHMS USED:

- 2D Lists (Dynamic Arrays): Used to load, access, and update rows from CSV files in memory.

- Dictionaries (Hash Maps): Used to group test scores by subject and calculate GPA in linear time.

- Tuples: Used to map filtered pending assignments back to their original row index.

- Iterative Simulation: Used to test class-by-class attendance changes around the 75% threshold.

- Timsort (Custom Key Sorting): Used to sort pending assignments chronologically by deadline date.



CSV FILES AUTOMATICALLY CREATED:

- Subjects.csv (Subject_Name, Credits, Classes_Held, Classes_Attended)

- Assignments.csv (Subject_Name, Assignment_Name, Deadline, Status)

- Grades.csv (Subject_Name, Exam_Name, Marks_Secured, Max_Marks)



HOW TO RUN:

1. Make sure Python 3 is installed on your computer.

2. Open a terminal or command prompt in the project folder.

3. Run the command: python main.py
