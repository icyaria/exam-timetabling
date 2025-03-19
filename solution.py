import csp
import pandas as pd
import time
from utils import F

def load_exam_data(file_path):
    #Φορτώνει τα μαθήματα απο το CSV
    df = pd.read_csv(file_path)
    return {
        "courses": df["Μάθημα"].tolist(),
        "semesters": df["Εξάμηνο"].tolist(),
        "professors": df["Καθηγητής"].tolist(),
        "difficult": df["Δύσκολο (TRUE/FALSE)"].tolist(),
        "lab": df["Εργαστήριο (TRUE/FALSE)"].tolist(),
    }

class Timetable(csp.CSP):
    
    def __init__(self, data):
        self.courses = data["courses"]
        self.data = {course: (data["semesters"][i], data["professors"][i], data["difficult"][i], data["lab"][i])
                         for i, course in enumerate(self.courses)}
        self.domains = {course: [(slot, day) for day in range(1, 22) for slot in range(1, 4)] for course in self.courses}
        self.neighbors = {course: [] for course in self.courses}

        # all courses are neighbors of each other
        for course1 in self.courses:
            for course2 in self.courses:
                if course1 != course2:
                    self.neighbors[course1].append(course2)

        self.counter = 0  # Tracks the number of times constraints is called

        csp.CSP.__init__(self, self.courses, self.domains, self.neighbors, self.constraints)

    def constraints(self, A, a, B, b):
        self.counter += 1

        # single slot constraint
        if a == b:
            return False

        # same semester coyrses must be on different days
        if a[1] == b[1] and self.data[A][0] == self.data[B][0]:
            return False

        # Lab constraints:

        # lecture with lab cannot be in the last slot
        if self.data[A][3] and a[0] == 3: 
            return False

        # cant have both courses with labs on the same day
        if self.data[A][3] and self.data[B][3] and a[1] == b[1]: 
                return False 

        # at least one course has a lab and they are on the same day
        if (self.data[A][3] or self.data[B][3]) and  a[1] == b[1]: 
            if self.data[A][3]:  # A has a lab
                if b[0] == a[0] + 1:  # Lab slot
                    return self.data[B][3] is True  # Only lab can occupy this slot
                if b[0] == a[0]:  # Lecture slot
                    return not self.data[B][3]  # No lab can occupy this slot
            if self.data[B][3]:  # B has a lab
                if a[0] == b[0] + 1:  # Lab slot
                    return self.data[A][3] is True  # Only lab can occupy this slot
                if a[0] == b[0]:  # Lecture slot
                    return not self.data[A][3]  # No lab can occupy this slot

        # courses by the same professor must be on different days
        if a[1] == b[1] and self.data[A][1] == self.data[B][1]:
            return False

        # difficult courses must be on different days
        if a[1] == b[1] and self.data[A][2] and self.data[B][2]:
            return False

        # difficult courses must be at least two days apart
        if abs(a[1] - b[1]) < 2 and self.data[A][2] and self.data[B][2]:
            return False

        return True

    def display(self, assignment):
        print("The result is: ")
        if assignment is None:
            print("Didn't find a solution")
        else:
            for y in range(1, 22):  # Iterate over days
                print(f"Ημέρα {y}")
                print("--------")
                used_slots = set()  # Keep track of slots that have been filled
                for x in range(1, 4):  # Iterate over slots
                    slot_assigned = False
                    for var in self.courses:
                        if assignment[var] == (x, y) and (x, y) not in used_slots:
                            slot_assigned = True
                            print(f"slot {x}:", var)
                            used_slots.add((x, y))  # Mark the slot as used
                            if self.data[var][3] and x < 3:  # If it has a lab and fits in the schedule
                                lab_slot = (x + 1, y)
                                print(f"slot {x + 1}: {var} Εργαστήριο")
                                used_slots.add(lab_slot)  # mark lab slot as used
                    if not slot_assigned and (x, y) not in used_slots:
                        print(f"slot {x}: -")  # empty slots
                print()  # Separate days visually

# Main 
if __name__ == '__main__':
    file_path = 'h3-data.csv'
    data = load_exam_data(file_path)
    timetable = Timetable(data)  # Initialize Timetable

    start_time = time.time()

    # Choose method to use:
    solution = csp.backtracking_search(timetable, csp.mrv, csp.lcv, csp.forward_checking) # fc with mrv
    # solution = csp.backtracking_search(timetable, csp.mrv, csp.lcv, csp.mac) #mac with mrv
    # solution = csp.min_conflicts(timetable)

    end_time = time.time()

    timetable.display(solution)
    print("Number of times constraints function was called:", timetable.counter)
    print()
    print("Total time:", end_time - start_time)
    print()


