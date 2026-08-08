from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "Guido van Rossum",
        "status": "Available"
    },
    {
        "id": 2,
        "title": "Linux Administration",
        "author": "Michael Jang",
        "status": "Available"
    },
    {
        "id": 3,
        "title": "Kubernetes Basics",
        "author": "Kelsey Hightower",
        "status": "Available"
    }
]

students = []

@app.route("/")
def home():
    return render_template(
        "index.html",
        books=books,
        students=students
    )


@app.route("/add-book", methods=["POST"])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")

    if title and author:
        new_book = {
            "id": len(books) + 1,
            "title": title,
            "author": author,
            "status": "Available"
        }

        books.append(new_book)

    return redirect(url_for("home"))


@app.route("/add-student", methods=["POST"])
def add_student():
    name = request.form.get("name")
    email = request.form.get("email")

    if name and email:
        students.append({
            "id": len(students) + 1,
            "name": name,
            "email": email
        })

    return redirect(url_for("home"))


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").lower()

    results = [
        book for book in books
        if keyword in book["title"].lower()
        or keyword in book["author"].lower()
    ]

    return render_template(
        "index.html",
        books=results,
        students=students,
        search_keyword=keyword
    )


@app.route("/issue/<int:book_id>")
def issue_book(book_id):
    for book in books:
        if book["id"] == book_id and book["status"] == "Available":
            book["status"] = "Issued"
            break

    return redirect(url_for("home"))


@app.route("/return/<int:book_id>")
def return_book(book_id):
    for book in books:
        if book["id"] == book_id and book["status"] == "Issued":
            book["status"] = "Available"
            break

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "application": "Library Management System"
    }, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
