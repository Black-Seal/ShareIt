<p align="center">
    <a target="_blank"><img alt='ShareIt Logo' src='src/static/images/ShareIt_Logo.jpg' width="250" height="250"/></a>
</p>

# ShareIt - A rental service for all things

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description
**ShareIt** is an innovative platform that enables community members to share underutilised resources. Users can list their unused items and borrow tools, equipment, and household goods from others in their community. By encouraging sustainable resource sharing, we aim to reduce waste and minimize redundant purchases.

## Features
- **Item Listing**: Users can list items for others to borrow.
- **Borrowing**: Browse the available listings and borrow items from your community.
- **User Registration**: Users can sign up to create accounts and manage their listings.
- **Item Reviews**: Lenders and borrowers can review each transaction.
- **Sustainable Living**: Promote eco-friendly sharing and reduce waste in the community.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Azure SQL Database (PaaS)
- **Cloud**: Microsoft Azure for SQL Database services

We'll be using venv as our virtual environment
```
pip install virtualenv
```

1. **Create virtual environment**

Mac
```
python3 -m venv myenv
```

Windows
```
python -m venv myenv
```

2. Activate virtual environment

Mac
```
source myenv/bin/activate
```

Windows
```
source myenv/Scripts/activate
```


3. Install required libraries & dependancies 
```
pip install -r requirements.txt
```

4. Set up the Flask environment:
```ssh
export FLASK_APP=app.py        # For macOS/Linux
set FLASK_APP=app.py           # For Windows
export FLASK_ENV=development   # Enables debug mode (macOS/Linux)
set FLASK_ENV=development      # (Windows)
```

5. Run the Flask app
```ssh
flask run
```

7. Access the app by navigating to http://127.0.0.1:5000/ in your browser.

# Usage
Once the app is running, users can:
- Register for a new account.
- List items they want to lend.
- Browse and borrow items listed by other users.
- Review items and transactions.

# Folder Structure
```
SHAREIT/                
│
├── data/                <------- Directory for datasets or input data files
│   ├── clean/           <------- Processed or cleaned data files
│   └── raw/             <------- Raw, unprocessed data files
│
├── notebooks/           <------- Jupyter notebooks 
│
├── sqlscripts/          <------- SQL scripts for database setup or queries
│
├── src/                 <------- Source code for the main application
│   ├── static/          <------- Static files (CSS, JavaScript, images, etc.)
│   ├── templates/       <------- HTML templates for rendering web pages
│   └── app.py           <------- Execution point
│
├── .gitignore           
│
├── README.md           
│
└── requirements.txt     

```

# Contributing

Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a feature branch: git checkout -b my-new-feature.
- Commit your changes: git commit -m 'Add some feature'.
- Push to the branch: git push origin my-new-feature.
- Submit a pull request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Contact

[**Public Domain**](https://nice-pebble-069dc3c00.5.azurestaticapps.net) (deprecated)