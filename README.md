# Use-case:

CRAN is a network of ftp and web servers around the world that store identical, up-to-date, versions of code and documentation for R. The R project uses these CRAN Servers to store R packages.
A CRAN server looks like: http://cran.r-project.org/src/contrib/. It is just a simple Apache Dir with a bunch of tar.gz files.

**PACKAGES file**

Every CRAN server contains a plain file listing all the packages in that server. You can access it using this URL: http://cran.r-project.org/src/contrib/PACKAGES

**Package URL format**

You can build the URL of every R package as: http://cran.rproject.org/src/contrib/[PACKAGE_NAME]_[PACKAGE_VERSION].tar.gz 

Example Package URL: http://cran.r-project.org/src/contrib/shape_1.4.1.tar.gz

Inside every package, after you uncompress it, there is a file called DESCRIPTION where you can get some extra information about the package:

## Aim
Create an application to index all the packages in a CRAN server with the following requirements:
1. Extract some information regarding every package and store it (you will need to get some info from the PACKAGES file and some other info from DESCRIPTION)
2. Create an API endpoint for search (something like /search?q=xyz) packages based package name which returns the list of all the packages you have searched
3. Implement the business logic needed for storing all the information (models, libs, DB structure...)

---
# System Requirements
python 3.7 or higher


# Development setup (for Ubuntu/Mac):
## Open Terminal :

* Ubuntu
  * `sudo apt-get install python-pip`
* MAC 
  
  This command should install python3 and pip3.
  * `brew install python@3.7`


## Clone Project to your directory
`git clone https://github.com/achugh95/cran.git`

`cd cran`

## Check python version on your development system
`python --version or python3 --version`


# Setup environment:
## 1. Create a virtual environment

  - `python3 -m venv <path>`

## 2. Activate virtual environment

  - `source <path_to_virtual_environment>/bin/activate`

## 3. Install requirements. Use the package manager pip to install the dependencies. 
`pip3 install -r requirements.txt`


## NOTE: Running the migrations will try to create tables in the `default` database.
  * If you have Postgres installed on your system, then please do the following:
    * Inside the parent directory cran, create a file cran/local_config.py. This will be at the same level as of settings.py
    * Define three variables in it:
      * DB_NAME='db-value'
      * DB_USER='user'
      * DB_PASSWORD='your-password'
  * The settings.py file uses these three variables to connect to the database. In that case, simply comment out the import statement of above variables in settings.py

  * Alternatively, you can use the sqlite database by changing the DATABASES dictionary in settings.py.

## 4. Run migrations

`python3 manage.py makemigrations`

`python3 manage.py migrate`

## 5. Run Project
Open terminal and run the following commands:

`python3 manage.py runserver`

---
## Run Tests

* To run the tests, from the parent directory:
  * `coverage run --source='.' manage.py test`
  
  NOTE: Add a flag `--omit='venv/*'` if you have created your virtual environment inside the project.

* To check the coverage report:
  * `coverage report`
  
---
# API 

### Command to populate package

`python3 manage.py populate_package`

### Curl for Search API

`curl --location --request GET 'localhost:8000/api/v1/package/search/?name=a'`

---
# Request Flow

Please check [this diagram](request_flow.jpg) for the expected request flow from an architectural perspective.


---
# Further Enhancements

**1. Using ElasticSearch to index the posts as this will help speed up the query on package name.**

**2. Using parallelism and batch processing while populating the packages in the database.**

**3. Increase test coverage. Currently, it is 80%.**
