from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB and table
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))

        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add.html")

@app.route("/view")
def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("view.html", students=students)

@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)
