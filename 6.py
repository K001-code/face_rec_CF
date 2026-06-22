#6
def manage_grade():
    grades ={"Jonh": "A","Mary": "B","Peter": "C"}
    grades["David"]="A+"
    grades.pop("Peter")
    return grades
final_grades = manage_grade()
print("Expected Outcome:",final_grades)