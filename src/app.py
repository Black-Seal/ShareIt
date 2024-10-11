from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Handle form submission logic here
        userid = request.form.get("userid")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        address = request.form.get("address")
        contactnumber = request.form.get("contactnumber")
        # You can add code here to store the user in a database or process the data
        return redirect(url_for("home"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
