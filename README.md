# Dynamic Table App
=======================

A simple database-driven web application built using FastHTML and Python.

## Overview
-----------

This application provides a basic CRUD (Create, Read, Update, Delete) interface for managing a clients database. The database is stored in memory using SQLite.

## Features
------------

* Create new clients with name, address, and email
* Read and display existing clients
* Update client information
* Delete clients

## Requirements
---------------

* Python 3.x
* FastHTML
* SQLite

## Installation
------------

1. Clone this repository: `git clone https://github.com/your-username/clients-app.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage
-----

1. Open a web browser and navigate to `http://localhost:5001`
2. Click on the "Clients" tab to view the list of clients
3. Click on the "Add" button to create a new client
4. Fill in the client information and click "Submit"
5. Click on a client's row to view and edit their information

## Code Structure
----------------

The application is built using a single Python file, `main.py`. This file contains the following components:

* Database setup and configuration
* Client dataclass definition
* FastHTML application setup and routing
* CRUD operations for clients

## Contributing
------------

Pull requests and issues are welcome! Please submit any changes or suggestions to the `main.py` file.

## License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.
