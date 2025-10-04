from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS (allow GET requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Read CSV data once at startup
students_data = []
with open("students.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert studentId to int
        row["studentId"] = int(row["studentId"])
        students_data.append(row)


@app.get("/api")
def get_students(class_: list[str] = Query(default=None, alias="class")):
    """
    Returns all students, or filters by ?class=1A&class=1B etc.
    """
    if class_:
        filtered = [s for s in students_data if s["class"] in class_]
        return {"students": filtered}
    return {"students": students_data}
