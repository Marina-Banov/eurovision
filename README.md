# eurovision

Python version: Python 3.9

You can initialize a virtual environment before project setup.  
To install the necessary packages run:
```
pip install flask python-dotenv flask-sqlalchemy flask-migrate flask-cors
```

Remember to create a `.env` file similar to `.env.example`.  
Run `flask db upgrade` to apply database migrations.
Run `flask run` to start the server.
