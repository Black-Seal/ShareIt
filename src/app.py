from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import re
from datetime import datetime

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

@app.route("/borrow_item/<int:item_id>", methods=["GET", "POST"])
def borrow_item(item_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the item details
    cursor.execute("SELECT Item_Name, Description, Price FROM dbo.Items WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    if not item:
        return "Item not found", 404

    # If form is submitted, process the borrowing
    if request.method == "POST":
        borrower_id = request.form.get("borrower_id")  # Fetch the borrower (logged-in user ID)
        lender_id = request.form.get("lender_id")      # Assuming you already know the lender ID from your logic
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Convert to date format and calculate the number of days
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end_date_obj - start_date_obj).days
        total_price = num_days * item[2]  # item[2] is the price from the fetched item

        # Insert into the Listings table
        query = """
        INSERT INTO dbo.listings (BorrowerID, LenderID, ItemID, StartDate, EndDate, ReturnFlag)
        VALUES (?, ?, ?, ?, ?, 0)
        """
        cursor.execute(query, (borrower_id, lender_id, item_id, start_date, end_date))
        conn.commit()
        conn.close()

        return redirect(url_for("success_page"))  # Redirect to success or listing page after transaction

    conn.close()
    return render_template("borrow_item.html", item=item)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Sanitize email input
        email = re.sub(r'[^\w\.\@]', '', email)

        # Connect to the database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM dbo.users WHERE Email = ?"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user.Password, password):
                    # Login successful
                    session["user_id"] = user.UserID  # Store user ID in session
                    session["user_email"] = user.Email
                    return redirect(url_for("listing"))
                else:
                    flash("Invalid email or password. Please try again.", "error")
            except Exception as e:
                print("Error during login:", e)
            finally:
                conn.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_email", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)    # Enable debug first so can track errors
