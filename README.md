# Simple blog application using flask
This is example repository to build lightweight blog server using Flask REST capabilities.

## Development server setup
1. Create and activate python virtual environment with pyhton version >= 3.8. Please check the [Link](https://docs.python.org/3/library/venv.html) for more information
2. Install packages by executing command `pip install -r dev-requirements.txt`
3. Install precommit hooks `pip install pre-commit && pre-commit install && pre-commit install --install-hooks`
4. Change the database config from the `config.py` file Please check [Connection URL format](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/config/#connection-url-format) for more info. Also if you face DB connection issue please install relevent connector library eg. for mysql `pip install mysqlclient` is required
5. Migrate database using `manage.py`
6. Run server by using `flask --app src.app run --debug`
