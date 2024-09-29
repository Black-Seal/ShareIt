<p align="center">
    <a target="_blank"><img alt='ShareIt Logo' src='static/images/ShareIt_Logo.jpg' width="250" height="250"/></a>
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

## Installation

1. Clone the repository:
```ssh
git clone git@github.com:Black-Seal/ShareIt.git
```

2. Create a virtual environment:
```ssh
python3 -m venv .venv
```

3. Activate the virtual environment:
- **macOS**
```ssh
source .venv/bin/activate
```
- **Windows**
```ssh
.\.venv\Scripts\Activate.ps1
```

4. Install the required dependencies:
```ssh
pip install -r requirements.txt
```

5. Set up the Flask environment:
```ssh
export FLASK_APP=app.py        # For macOS/Linux
set FLASK_APP=app.py           # For Windows
export FLASK_ENV=development   # Enables debug mode (macOS/Linux)
set FLASK_ENV=development      # (Windows)
```

6. Run the Flask app
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
project/
│
├── static/                     # Static files (CSS, images)
│   ├── images/                 # Logo and other images
│   └── styles.css              # Custom styles for the app
│
├── templates/                  # HTML templates for rendering web pages
│   └── base.html
│   └── home.html
│   └── about.html
│
├── app.py                      # Main Flask app
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
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