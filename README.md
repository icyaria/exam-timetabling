---

## Exam Timetabling Problem

This repository contains a solution to the [Exam Timetabling Problem](chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://cgi.di.uoa.gr/~ys02/askiseis2024/h3-2024.pdf) using **Constraint Satisfaction Problems (CSPs)**. It was part of the 2024-2025 [AI1 course](https://cgi.di.uoa.gr/~ys02/) The goal is to generate an exam timetable for a given set of courses, professors, and constraints, such as room availability, professor schedules, and student workload, all while adhering to specific rules like avoiding conflicts between courses from the same semester or professor.

### Problem Definition

The problem consists of assigning exam times and dates for a set of courses during a 21-day examination period, with the following constraints:
- Each exam lasts 3 hours.
- Exams are scheduled in one of three available time slots per day: 9 AM - 12 PM, 12 PM - 3 PM, or 3 PM - 6 PM.
- A single room is available for all exams, so no two exams can overlap in time.
- Exams for the same semester must be scheduled on different days.
- Some courses have a laboratory component, which must be scheduled immediately after the theory exam on the same day.
- Difficult courses must be spaced at least 2 days apart.
- Exams for courses taught by the same professor must be on different days.

### Approach

To solve this problem, the following **CSP algorithms** are implemented and applied:
1. **Forward Checking (FC)**: This technique propagates constraints during the assignment process, checking if an assignment is consistent with the existing ones.
2. **Maintaining Arc Consistency (MAC)**: This enhances forward checking by ensuring that all variable domains are arc-consistent before each assignment.
3. **Min-Conflicts (MINCONFLICTS)**: A heuristic-based algorithm that iteratively selects variables with the most conflicts and assigns them values that minimize conflicts.

We also use heuristics such as **Minimum Remaining Values (MRV)** for dynamic variable ordering and **Least Constraining Value (LCV)** for value ordering.

### Files
- `solution.py`: Contains the implementation of the CSP problem, including loading the course data, defining the CSP model, and solving the timetable problem using the algorithms.
- `csp.py`: Defines the CSP class and related methods for handling variable assignments, constraints, and inference techniques like forward checking and arc consistency.
- `search.py`: Implements search algorithms such as backtracking and min-conflicts for CSP solutions.
- `utils.py`: Utility functions for handling various tasks such as counting, removing duplicates, and handling statistical operations.

### Running the Solution

To run the exam timetable solver, you need to load the data from a CSV file that contains the course information. The solution uses **Pandas** to read the CSV and organize the data into the correct format.

Run the script in `solution.py` by providing the path to the CSV file:
```bash
python solution.py
```

This will print the timetable, showing the assignments of courses to specific time slots across the 21-day exam period.

### Requirements
- Python 3.x
- Pandas library for reading the CSV (`pip install pandas`)

### Customization
You can customize the problem by modifying the constraints or adapting the input CSV file format to include additional information (e.g., number of students per course, specific lab constraints).

---
