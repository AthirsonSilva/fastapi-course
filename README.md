# Python and FastAPI Web Services Development Course for Beginners

This project is a complete course on building web services with Python and FastAPI, designed for beginners. It covers the fundamentals of web services, including RESTful APIs, HTTP requests and responses, and how to use FastAPI to build robust, scalable web services.

## Features

- Covers the basics of web services and RESTful APIs
- Uses Python and FastAPI to build a fully functional web service
- Covers database integration using SQLAlchemy
- Includes testing and deployment best practices

## Architecture

The application is built using Python and the FastAPI framework. It consists of several layers:

- `main.py`: Entry point of the application
- `database.py`: Interface to the database
- `routes`: Folder with several file to each resource of the project containing all business logic
- `oauth2`: Cyber security, authentication and authorization logic

## Usage
The API endpoints can be accessed using any HTTP client software or web browser. The API documentation is available at http://localhost:8000/docs.

![Screenshot_20230413_194634](https://user-images.githubusercontent.com/84593887/231899211-04501d76-490b-4567-853b-06e141eb18f6.png)

## Database

The project uses SQLAlchemy as the database ORM (Object-Relational Mapping) tool to interact with databases. It supports various databases such as SQLite, MySQL, PostgreSQL, Oracle, Microsoft SQL Server, and others. For this project, we'll be using PostgresSQL

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip
- Postgres

### Installation

Install dependencies

```sh
cd fastapi-web-services
pip install -r requirements.txt
```

Run the project

```sh
uvicorn main:app --reload
```

The application will start and be available at http://localhost:8000.

Contributing
Contributions are welcome! Just fork the project and make a pull request that I will review.

License
This project is licensed under the MIT License. See the LICENSE file for details.
