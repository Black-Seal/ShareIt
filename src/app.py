from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import re
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY", "fallback-secret-key"
)  # 'fallback-secret-key' is used if env variable is not set

DATABASE_CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sit-dev-shareit.database.windows.net,1433;"
    "Database=dev-shareit;"
    "Uid=jjask-admin;"
    "Pwd={5h:oF9I!2dfH7hB};"  # SENSITIVE
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
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
        email = re.sub(r"[^\w\.\@]", "", email)  # Remove unwanted characters from email
        contactnumber = re.sub(
            r"\D", "", contactnumber
        )  # Keep only numbers for contact number
        password = password.strip()  # Strip whitespace from password

        # Hash the password securely using Werkzeug
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=16
        )

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
                cursor.execute(
                    query, (firstname, lastname, email, hashed_password, contactnumber)
                )
                conn.commit()
            except Exception as e:
                print("Error inserting data:", e)
            finally:
                conn.close()

        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/listing")
def listing():
    # Get the current user ID from the session
    current_user_id = session.get("user_id")
    if not current_user_id:
        flash("You must be logged in to view the listings", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    listings = []
    
    if conn:
        try:
            cursor = conn.cursor()

            # Updated SQL query to exclude items listed by the current user (Lender/UserID check)
            query = """
            SELECT i.ItemID, i.ItemName, i.Description, i.Price
            FROM dbo.items i
            LEFT JOIN dbo.listings l ON i.ItemID = l.ItemID
            WHERE (l.ItemID IS NULL OR l.ReturnFlag = 1)
            AND i.UserID != ?
            """
            cursor.execute(query, (current_user_id,))
            listings = cursor.fetchall()  # Fetch all available listings excluding the user's own items
        except Exception as e:
            print("Error fetching listings:", e)
        finally:
            conn.close()

    # Render the listings in the template
    return render_template("listing.html", listings=listings)

@app.route("/listitem", methods=["GET", "POST"])
def listitem():
    if request.method == "POST":
        # Check if user is logged in
        user_id = session.get("user_id")
        if not user_id:
            return redirect(
                url_for("login")
            )  # Redirect to login if user is not logged in

        # Retrieve form data
        item_name = request.form.get("ItemName")
        item_description = request.form.get("Description")
        item_price = request.form.get("Price")

        # Validate that the data is present and correct
        if not item_name or not item_description or not item_price:
            return "Please fill in all fields", 400  # Error message for missing fields

        # Connect to the database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Insert the new listing into the `items` table
                query = """
                INSERT INTO dbo.items (ItemName, Description, Price, UserID)
                VALUES (?, ?, ?, ?)
                """
                cursor.execute(
                    query, (item_name, item_description, item_price, user_id)
                )
                conn.commit()
            except Exception as e:
                print("Error inserting listing:", e)
                return (
                    "Failed to add listing",
                    500,
                )  # Error message for DB insertion issues
            finally:
                conn.close()

            return redirect(
                url_for("listing")
            )  # Redirect to the listing page after successful addition

    # Render the listing form for GET requests
    return render_template("listitem.html")

@app.route("/borrow_item/<int:item_id>", methods=["GET", "POST"])
def borrow_item(item_id):
    # Check if the user is logged in
    borrower_id = session.get("user_id")
    if not borrower_id:
        flash("You must be logged in to borrow an item", "error")
        return redirect(url_for("login"))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the item details including the LenderID
    cursor.execute(
        "SELECT ItemName, Description, Price, UserID FROM dbo.Items WHERE ItemID = ?",
        (item_id,),
    )
    item = cursor.fetchone()
    if not item:
        return "Item not found", 404

    # Item details
    item_name, item_description, item_price, lender_id = item  # lender_id is the UserID of the owner of the item

    if request.method == "POST":
        start_date = request.form.get("StartDate")
        end_date = request.form.get("EndDate")

        # Convert to date format and calculate the number of days
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end_date_obj - start_date_obj).days
        total_price = num_days * item_price  # Calculate the total price

        # Insert into the Listings table with ReturnFlag = 0 (borrowed)
        query = """
        INSERT INTO dbo.listings (BorrowerID, LenderID, ItemID, StartDate, EndDate, ReturnFlag)
        VALUES (?, ?, ?, ?, ?, 0)
        """
        cursor.execute(query, (borrower_id, lender_id, item_id, start_date, end_date))
        conn.commit()

        # Close the connection
        conn.close()

        flash("Item borrowed successfully!", "success")
        return redirect(url_for("listing"))

    # Close the connection
    conn.close()
    return render_template(
        "borrow_item.html",
        item_name=item_name,
        item_description=item_description,
        item_price=item_price,
        item_id=item_id,
        LenderID=lender_id,
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Sanitize email input
        email = re.sub(r"[^\w\.\@]", "", email)

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


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(
            url_for("login")
        )  # Redirect to login if the user is not logged in

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute(
        "SELECT FirstName, LastName FROM dbo.users WHERE UserID = ?", (user_id,)
    )
    user = cursor.fetchone()

    # Fetch the listings created by the user (items they listed)
    cursor.execute(
        """
        SELECT ItemID, ItemName, Description 
        FROM dbo.items 
        WHERE UserID = ?
    """,
        (user_id,),
    )
    user_listings = cursor.fetchall()

    # Fetch the items borrowed by the user
    cursor.execute(
        """
        SELECT i.ItemName, i.Description, l.StartDate, l.EndDate, l.ItemID
        FROM dbo.listings l
        JOIN dbo.items i ON l.ItemID = i.ItemID
        WHERE l.BorrowerID = ? AND l.ReturnFlag = 0
    """,
        (user_id,),
    )
    borrowed_items = cursor.fetchall()

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        user_listings=user_listings,
        borrowed_items=borrowed_items,
    )

@app.route("/update_item/<int:item_id>", methods=["GET", "POST"])
def update_item(item_id):
    user_id = session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the item is currently borrowed (ReturnFlag = 0)
    cursor.execute(
        "SELECT LenderID, BorrowerID, ReturnFlag FROM dbo.listings WHERE ItemID = ?", (item_id,)
    )
    listing = cursor.fetchone()

    # Prevent update if the item is currently borrowed (ReturnFlag = 0)
    if listing and listing[2] == 0:
        flash("You cannot update this item because it is currently borrowed.", "error")
        return redirect(url_for("profile"))

    # Fetch item details from the items table
    cursor.execute(
        "SELECT ItemName, Description, Price FROM dbo.items WHERE ItemID = ?", (item_id,)
    )
    item_details = cursor.fetchone()

    if not item_details:
        flash("Item not found.", "error")
        return redirect(url_for("profile"))

    # If the request method is POST, update the item (name, description, and price)
    if request.method == "POST":
        item_name = request.form.get("item_name")
        description = request.form.get("description")
        price = request.form.get("price")  # Fetch the price from the form

        # Ensure that item_name, description, and price are not empty
        if not item_name or not description or not price:
            flash("Item name, description, and price are required.", "error")
            return redirect(url_for("update_item", item_id=item_id))

        # Update the item details in the database (including price)
        cursor.execute(
            "UPDATE dbo.items SET ItemName = ?, Description = ?, Price = ? WHERE ItemID = ?",
            (item_name, description, price, item_id),
        )
        conn.commit()
        conn.close()

        # Redirect to the profile page after updating the item
        flash("Item updated successfully.", "info")
        return redirect(url_for("profile"))

    conn.close()

    # Pass the item details to the template
    item = {
        "ItemID": item_id,
        "ItemName": item_details.ItemName,
        "Description": item_details.Description,
        "Price": item_details.Price,  # Include price
    }
    return render_template("update_item.html", item=item)

@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    user_id = session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the listing details to check if the item is borrowed or not
    cursor.execute(
        "SELECT LenderID, BorrowerID, ReturnFlag FROM dbo.listings WHERE ItemID = ?", (item_id,)
    )
    listing = cursor.fetchone()

    # If the item is listed and the current user is not the lender, unauthorized access
    if listing and listing[0] != user_id:
        flash("Unauthorized to delete this item.", "error")
        return redirect(url_for("profile"))

    # If the item is currently borrowed (ReturnFlag = 0), deny deletion
    if listing and listing[2] == 0:
        flash("You cannot delete this item while it is being borrowed.", "error")
        return redirect(url_for("profile"))

    # Step 1: Delete any related listings that reference this item
    cursor.execute("DELETE FROM dbo.listings WHERE ItemID = ?", (item_id,))
    conn.commit()

    # Step 2: Delete the item from the items table
    cursor.execute("DELETE FROM dbo.items WHERE ItemID = ?", (item_id,))
    conn.commit()

    conn.close()

    flash("Item and its associated listings deleted successfully.", "info")
    return redirect(url_for("profile"))

@app.route("/mark_as_returned", methods=["POST"])
def mark_as_returned():
    # Get the BorrowerID from the session (user_id is the BorrowerID)
    borrower_id = session.get("user_id")
    
    if not borrower_id:
        return redirect(url_for("login"))  # Redirect if the user is not logged in

    # Get the list of item IDs marked as returned
    returned_items = request.form.getlist("return_items")

    print(f"Returned items: {returned_items}")  # Debugging: Check what items were selected

    if not returned_items or not all(returned_items):
        flash("No items selected for return.", "error")
        return redirect(url_for("profile"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update the ReturnFlag to 1 (returned) for the selected items
        query = """
        UPDATE dbo.listings
        SET ReturnFlag = 1
        WHERE ItemID = ? AND BorrowerID = ?
        """
        for item_id in returned_items:
            print(f"Updating ReturnFlag for ItemID: {item_id}, BorrowerID: {borrower_id}")  # Debugging
            cursor.execute(query, (item_id, borrower_id))
        
        conn.commit()
        flash("Items marked as returned successfully.", "success")
    except Exception as e:
        print("Error marking items as returned:", e)
        flash("An error occurred while processing the return.", "error")
    finally:
        conn.close()

    return redirect(url_for("profile"))

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug first so can track errors
