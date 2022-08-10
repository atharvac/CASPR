# CASPR
**CASPR** is a Code Trust Auditing framework. It provides an organisation with necessary tools to verify, validate and 
attribute changes happening to their code repositories and make it part of their Build Process. 

## Requirements - SPAR
1) Python >= 3.6
2) PIP
3) Pipenv

## Installation - SPAR

Setup SPAR verification server first so that you can upload your trusted keys.
Clone the repository and open the SPAR directory in your terminal / CMD.

Create a .env file in the directory. Please refer to the .env.example file.

Example
```bash
APP_CONFIG=spar.config.DevelopmentConfig
FLASK_ENV=development
DB_URL=postgresql+psycopg2://postgres:test@localhost/spar
SECRET_KEY=super-secret
```

Use Pipenv to install the dependancies:
```bash
pipenv install
```
If there are issues in the pipenv lock file, please use:
```bash
pipenv install -r requirements.txt
```

After the installation of the dependancies and creation of the virtual environment, use the following command to use the 
environment:
```bash
pipenv shell
```
Once the environment is activated, run the following command to setup your database:
```bash
flask db upgrade
```
Run the following to start the server:
```bash
flask run -h 0.0.0.0 -p 5000
```
The server will start listening at [http://localhost:5000/](http://localhost:5000/)

On first run, the server will ask you to setup an admin account. Please go through the process as indicated on screen.
## Usage


## License
[MIT](https://choosealicense.com/licenses/mit/)
