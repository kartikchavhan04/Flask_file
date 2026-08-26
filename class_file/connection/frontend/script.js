// Flask backend URL

const API_URL = "http://127.0.0.1:5000";


// =====================================================
// GET STUDENTS
// =====================================================

function getStudents() {

    fetch(`${API_URL}/students`)

        .then(response => {

            if (!response.ok) {
                throw new Error("Failed to get students");
            }

            return response.json();
        })

        .then(students => {

            const table = document.getElementById("studentTable");

            table.innerHTML = "";

            students.forEach(student => {

                const row = `
                    <tr>

                        <td>${student.id}</td>

                        <td>${student.name}</td>

                        <td>${student.email}</td>

                        <td>${student.marks}</td>

                        <td>

                            <button onclick="deleteStudent(${student.id})">
                                Delete
                            </button>

                        </td>

                    </tr>
                `;

                table.innerHTML += row;

            });

        })

        .catch(error => {

            console.error("Error:", error);

            alert("Unable to load students");

        });
}


// =====================================================
// POST - ADD STUDENT
// =====================================================

document
    .getElementById("studentForm")
    .addEventListener("submit", function(event) {

        event.preventDefault();


        const name = document.getElementById("name").value;

        const email = document.getElementById("email").value;

        const marks = document.getElementById("marks").value;


        fetch(`${API_URL}/student`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                name: name,

                email: email,

                marks: Number(marks)

            })

        })

        .then(response => response.json())

        .then(data => {

            console.log(data);

            alert(data.message);

            document
                .getElementById("studentForm")
                .reset();

            getStudents();

        })

        .catch(error => {

            console.error("Error:", error);

            alert("Unable to add student");

        });

    });


// =====================================================
// PUT - UPDATE STUDENT
// =====================================================

document
    .getElementById("updateForm")
    .addEventListener("submit", function(event) {

        event.preventDefault();


        const id = document.getElementById("updateId").value;

        const name = document.getElementById("updateName").value;

        const email = document.getElementById("updateEmail").value;

        const marks = document.getElementById("updateMarks").value;


        fetch(`${API_URL}/student/${id}`, {

            method: "PUT",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                name: name,

                email: email,

                marks: Number(marks)

            })

        })

        .then(response => response.json())

        .then(data => {

            console.log(data);

            alert(data.message);

            document
                .getElementById("updateForm")
                .reset();

            getStudents();

        })

        .catch(error => {

            console.error("Error:", error);

            alert("Unable to update student");

        });

    });


// =====================================================
// DELETE STUDENT
// =====================================================

function deleteStudent(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this student?"
    );


    if (!confirmDelete) {

        return;

    }


    fetch(`${API_URL}/student/${id}`, {

        method: "DELETE"

    })

    .then(response => response.json())

    .then(data => {

        console.log(data);

        alert(data.message);

        getStudents();

    })

    .catch(error => {

        console.error("Error:", error);

        alert("Unable to delete student");

    });

}