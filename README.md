# Flask Inventory Management System

A Flask REST API for managing a retail company's inventory. The system also integrates with the OpenFoodFacts API and provides a command-line interface (CLI).

## Features

- View all inventory items
- View a single inventory item
- Add inventory items
- Update inventory items
- Delete inventory items
- Search OpenFoodFacts products by barcode
- Search OpenFoodFacts products by name
- Import OpenFoodFacts products into inventory
- CLI for interacting with the API
- Automated tests using pytest

## Technologies

- Python
- Flask
- Requests
- Pytest
- OpenFoodFacts API

## Installation

Clone the repository:

```bash
git clone https://github.com/Abdikalolo/flask-management-system-sum-lab.git
cd flask-management-system-sum-lab

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install the dependencies:

pip install -r requirements.txt
Running the Flask API

Start the server:

python app.py

The API runs at:

http://127.0.0.1:5000
API Routes
Method	Route	Description
GET	/inventory	Get all inventory
GET	/inventory/<id>	Get one inventory item
POST	/inventory	Add an inventory item
PATCH	/inventory/<id>	Update an inventory item
DELETE	/inventory/<id>	Delete an inventory item
GET	/external-products/barcode/<barcode>	Search OpenFoodFacts by barcode
GET	/external-products/search?name=<name>	Search OpenFoodFacts by name
POST	/inventory/import	Import an OpenFoodFacts product
Running the CLI

With the Flask server running, open another terminal and activate the virtual environment:

source .venv/bin/activate

Then run:

python cli.py

The CLI can be used to view, add, update, and delete inventory items.

Testing

The project uses pytest for automated testing.

Run all tests:

pytest

The test suite covers:

Inventory retrieval
Inventory creation
Inventory updates
Inventory deletion
Error handling
OpenFoodFacts barcode search
OpenFoodFacts name search
OpenFoodFacts product import

All 14 tests pass.

Data Storage

The inventory is stored in a Python list in memory. This is a simulated database for the project.

Data is reset when the Flask application is restarted.

Git Workflow

The project uses Git branches for development.

Feature branches were used for:

feature-inventory-crud
feature-testing

Changes were committed, pushed to GitHub, reviewed through a Pull Request, and merged into main.

Project Structure
flask-management-system-sum-lab/
├── app.py
├── cli.py
├── README.md
├── requirements.txt
├── .gitignore
└── tests/
    ├── __init__.py
    └── test_app.py
Author

Abdi Hussein

GitHub: https://github.com/Abdikalolo