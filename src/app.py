from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

DATABASE_CONNECTION_STRING = (
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=tcp:sit-dev-shareit.database.windows.net,1433;'
    'Database=dev-shareit;'
    'Uid=jjask-admin;'
    'Pwd={5h:oF9I!2dfH7hB};'    # SENSITIVE
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

def get_db_connection():
    try:
        connection = pyodbc.connect(DATABASE_CONNECTION_STRING)
        return connection
    except Exception as e:
        print("Error connecting to database:", e)
        return None

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
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        address = request.form.get("address")
        contactnumber = request.form.get("contactnumber")

        # Connect to the database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # SQL script to insert user data into the 'users' table
                # UserID is PK so excluded here
                query = """
                INSERT INTO dbo.users (FirstName, LastName, Email, Address, Contact)
                VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (firstname, lastname, email, address, contactnumber))
                conn.commit()
            except Exception as e:
                print("Error inserting data:", e)
            finally:
                conn.close()
        return redirect(url_for("home"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)    # Enable debug first so can track errors
