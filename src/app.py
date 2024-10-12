from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from werkzeug.security import generate_password_hash
import re

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
        password = request.form.get("password")
        contactnumber = request.form.get("contactnumber")

        # Sanitizing inputs (you can add more rules based on your specific needs)
        email = re.sub(r'[^\w\.\@]', '', email)  # Remove unwanted characters from email
        contactnumber = re.sub(r'\D', '', contactnumber)  # Keep only numbers for contact number
        password = password.strip()  # Strip whitespace from password

        # Hash the password securely using Werkzeug
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Connect to the database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # SQL script to insert user data into the 'users' table
                # We assume there's a 'Password' column in the 'users' table
                query = """
                INSERT INTO dbo.users (FirstName, LastName, Email, Password, Contact)
                VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (firstname, lastname, email, hashed_password, contactnumber))
                conn.commit()
            except Exception as e:
                print("Error inserting data:", e)
            finally:
                conn.close()

        return redirect(url_for("home"))
    
    return render_template("register.html")

@app.route("/listing")
def listing():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Assuming there is a table called 'items' that stores the listings
            query = """
            SELECT TOP 10 * FROM dbo.items
            ORDER BY ItemID DESC
            """
            cursor.execute(query)
            listings = cursor.fetchall()  # Fetch the first set of listings
        except Exception as e:
            print("Error fetching listings:", e)
            listings = []
        finally:
            conn.close()
    else:
        listings = []
    
    # Render the listings in the template
    return render_template("listing.html", listings=listings)

@app.route("/load-more-listings")
def load_more_listings():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Fetch the next set of listings
            query = f"""
            SELECT * FROM dbo.items
            ORDER BY ItemID DESC
            OFFSET {offset} ROWS
            FETCH NEXT {per_page} ROWS ONLY
            """
            cursor.execute(query)
            listings = cursor.fetchall()
            # Convert the results to a JSON serializable format
            listings_data = [
                {
                    'name': listing.ItemName,
                    'description': listing.ItemDescription
                    # Add other necessary fields here
                } for listing in listings
            ]
        except Exception as e:
            print("Error fetching more listings:", e)
            listings_data = []
        finally:
            conn.close()
    else:
        listings_data = []
    
    return {'listings': listings_data}


@app.route('/listitem', methods=['GET', 'POST'])
def listitem():
    # Logic to render the page where users can add a new listing
    return render_template('listitem.html')  # Assuming this is the page for adding a new listing


if __name__ == "__main__":
    app.run(debug=True)    # Enable debug first so can track errors
