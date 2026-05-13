import { useState, useEffect } from "react";

function App() {

  // Store input fields
  const [form, setForm] = useState({
    name: "",
    course: ""
  });

  // Store students from backend
  const [students, setStudents] = useState([]);

  // Handle input changes
  function handleChange(e) {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

  // Fetch students from backend
  async function getStudents() {

    const response = await fetch("http://localhost:8000/students");

    const data = await response.json();

    setStudents(data);
  }

  // Add student
  async function addStudent() {

    await fetch("http://localhost:8000/add", {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(form)
    });

    // Clear input fields
    setForm({
      name: "",
      course: ""
    });

    // Reload students
    getStudents();
  }

  // Delete student
  async function deleteStudent(id) {

    await fetch(`http://localhost:8000/delete/${id}`, {
      method: "DELETE"
    });

    getStudents();
  }

  // Run once when page loads
  useEffect(() => {
    getStudents();
  }, []);

  return (
    <div style={{ padding: "20px" }}>

      <h1>Student Manager</h1>

      {/* Input Fields */}
      <input
        type="text"
        name="name"
        placeholder="Enter Name"
        value={form.name}
        onChange={handleChange}
      />

      <input
        type="text"
        name="course"
        placeholder="Enter Course"
        value={form.course}
        onChange={handleChange}
      />

      <button onClick={addStudent}>
        Add Student
      </button>

      <hr />

      {/* Student List */}
      <h2>Students</h2>

      {students.map((student) => (

        <div key={student.id}>

          <p>
            {student.name} - {student.course}
          </p>

          <button onClick={() => deleteStudent(student.id)}>
            Delete
          </button>

        </div>

      ))}

    </div>
  );
}

export default App;
