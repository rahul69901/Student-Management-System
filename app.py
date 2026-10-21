from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password@123",
        database="student_db"
    )


@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    roll_no = request.form["roll_no"]
    course = request.form["course"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, roll_no, course) VALUES (%s, %s, %s, %s)",
        (name, age, roll_no, course)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        roll_no = request.form["roll_no"]
        course = request.form["course"]

        cursor.execute(
            "UPDATE students SET name=%s, age=%s, roll_no=%s, course=%s WHERE id=%s",
            (name, age, roll_no, course, id)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student is None:
        return "Student not found", 404

    return render_template("edit.html", student=student)


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)