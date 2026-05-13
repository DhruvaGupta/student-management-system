# 1. IMPORTS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sqlalchemy import create_engine, text

from urllib.parse import quote_plus


# 2. CREATE FASTAPI APP
app = FastAPI()


# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 4. DATABASE CONNECTION
password = quote_plus("Kanika@07")

DATABASE_URL = f"mysql+mysqlconnector://root:{password}@localhost/student_db"

engine = create_engine(DATABASE_URL)


# 5. INPUT MODEL
class Student(BaseModel):
    name: str
    course: str


# 6. HOME ROUTE
@app.get("/")
def home():

    return {
        "message": "Backend Running"
    }


# 7. ADD STUDENT API
@app.post("/add")
def add_student(student: Student):

    connection = engine.connect()

    connection.execute(
        text("""
            INSERT INTO students(name, course)
            VALUES (:name, :course)
        """),
        {
            "name": student.name,
            "course": student.course
        }
    )

    connection.commit()

    connection.close()

    return {
        "message": "Student Added"
    }


# 8. GET STUDENTS API
@app.get("/students")
def get_students():

    connection = engine.connect()

    result = connection.execute(
        text("SELECT * FROM students")
    )

    data = []

    for row in result:

        data.append({
            "id": row.id,
            "name": row.name,
            "course": row.course
        })

    connection.close()

    return data


# 9. DELETE STUDENT API
@app.delete("/delete/{student_id}")
def delete_student(student_id: int):

    connection = engine.connect()

    connection.execute(
        text("""
            DELETE FROM students
            WHERE id = :id
        """),
        {
            "id": student_id
        }
    )

    connection.commit()

    connection.close()

    return {
        "message": "Student Deleted"
    }
