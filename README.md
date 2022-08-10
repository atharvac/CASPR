# CASPR
**CASPR** is a Code Trust Auditing framework. It provides an organisation with necessary tools to verify, validate and attribute changes happening to their code repositories and make it part of their Build Process. 

## Requirements - SPAR
1) Python >= 3.6
2) PIP
3) Pipenv
4) Postman (Optional)

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

After the installation of the dependancies and creation of the virtual environment, use the following command to use the environment:
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
1) Download the Postman collection: [SPAR_collection](https://www.getpostman.com/collections/b08308d274989db8cac8)
2) Import the Postman collection.
3) Login to the SPAR server.
4) Click on "Create Access Token".
5) Enter a name and create a new Access Token.
6) Copy the access token in green at the top.
7) Edit the SPAR collection in Postman, go to variables and set the access_token to the one you have copied.
8) Set the server_url to your server base URL.
9) Generate a gpg keypair using the following command:
```bash
gpg --full-generate-key
```
10) Export the generated key using the following command:
```bash
gpg --export -a "demo@example.com" > public.key
```
11) Copy your fingerprint from the following command:
```bash
gpg --list-keys

Output:
pub   rsa3072 2022-07-14 [SC]
      3C37CC8474AE4160751C663AE1304A151744A119
uid           [ultimate] Demo <demo@example.com>
sub   rsa3072 2022-07-14 [E]
```
Here 3C37CC8474AE4160751C663AE1304A151744A119 is the fingerprint.

12) In the same directory, download this python file: [replace_rewlines.py](https://gist.github.com/atharvac/12f0a1b4cf2d52242fdd57b7fa85c033)
13) Run the file using the following command:
```bash
python replace_newlines.py
```
14) Open the "Upload Signing Public Key" postman request.
15) In JSON body, paste the fingerprint from step 11, and public key output from step 13.
16) Click on send. Your Public key will be registered.

### Now, we will set the Server URL and the access token in the remote repository.

### Github
1) Go to the repository you want to add the CASS scripts to.
2) Go to settings -> secrets -> actions -> New repository secret
3) Set name as: **SERVER_API_URL** and the value as **<server_url>/api/get-signing-key**
4) Create another repository secret Name: **ACCESS_TOKEN** value: **<Your access token from SPAR>**

### GitLab
1) Go to the repository you want to add the CASS scripts to.
2) Go to settings -> CI/CD -> Variables -> Expand -> Add Variable.
3) Set key as: **SERVER_API_URL** and the value as **<server_url>/api/get-signing-key**
4) Create another repository secret key: **ACCESS_TOKEN** value: **<Your access token from SPAR>**

### BitBucket
1) Go to the repository you want to add the CASS scripts to.
2) Go to Repository settings -> Pipelines -> Repository Variables.
3) Set name as: **SERVER_API_URL** and the value as **<server_url>/api/get-signing-key**
4) Create another repository secret Name: **ACCESS_TOKEN** value: **<Your access token from SPAR>**

#### Now your repository is ready to use the SPAR server. Please refer to the installation of CASS scripts.

## Installation (CASS)
Follow the documentation for whichever remote repository you are using.

### GitHub
1) Go to the CASS/github directory
2) Run yarn install
3) Run yarn build
4) Copy the directory: .github to your repository
5) Copy the files: action.yml, package.json dist/index.js to your repository.
6) Edit action.yml, under "runs" set main to the index.js file relative to your repository root.
7) If you already have github actions configured, please add the actions in your yml file.

### GitLab
1) Copy the .gitlab-ci.yml, index.js and package.json files in your repository.
2) Setup your runner to run for the tag: local or change the tag name in the gitlab-ci.yml file.
3) If you add the package.json and index.js files in a folder, edit the gitlab-ci.yml script tag to reflect the change.
```yml
  script:
    - npm install
    - git show --pretty=raw -s $CI_COMMIT_SHA | node folder/index.js
```

### BitBucket
1) Copy the bitbucket-pipelines.yml, index.js and package.json files in your repository.
2) If you add the package.json and index.js files in a folder, edit the bitbucket-pipelines.yml script tag to reflect the change.
```yml
   script:
     - npm install
     - git show --pretty=raw -s $BITBUCKET_COMMIT
     - git show --pretty=raw -s $BITBUCKET_COMMIT | node folder/index.js
```

## License
[MIT](https://choosealicense.com/licenses/mit/)