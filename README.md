# eurovision

Python version: Python 3.9

You can initialize a virtual environment before project setup. 

To install the necessary packages run:
```
pip install flask python-dotenv flask-sqlalchemy flask-migrate flask-cors
```

Remember to create a `.env` file similar to `.env.example`.

To apply database migrations run:
```
flask db upgrade
```
To apply database seeds run:
```
flask seed
```
To start the server run:
``` 
flask run
```
