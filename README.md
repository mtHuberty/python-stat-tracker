# python-stat-tracker
Python web scraper to track WoW PvP stats from the top ranking players in each category (2v2, 3v3, RBGs). Currently, only a backend web-scraping portion is under construction. A frontend and possibly discord bot will be built to display the data in the near future!

### Note about Browsers
Make sure you have Chrome or Firefox installed on your system. You can choose which browser is used by editing the config file. 

### Note about the browser drivers
Currently, both Mac and Windows drivers are in the folder python-stat-tracker/chromedrivers/ and the python script will detect which environment it's running on and use the appropriate driver for the chosen browser, so it should work out of the box on Mac/Windows. Linux support coming soon (before we move it to a Linux box).

---

### Getting started with development

#### Get virtualenv
It's highly recommended to use virtualenv to manage your python packages. Assuming you already have python3.4+ and pip, and have cloned this repo:
- Make sure pip is tied the correct version of Python (3.4+) by typing `pip --version` in your console. If it's not, you may need to use pip3 or reinstall python or pip.
- Run `pip install virtualenv` (or `pip install virtualenv --user` on a Mac)
- `cd` into the python-stat-tracker directory
- Run `virtualenv env` - This will create a new virtual environment in a folder called "env", along with whichever python version installed the virtualenv package. 
- This next part depends on your OS
  - For windows, (on powershell), Run `.\env\bin\activate`. If you get permission problems, first run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` and choose "Yes to All". This should let you execute the activate script.
  - For Mac, Run `source env/bin/activate`
- You should see (env) at the beginning of your shell prompt now, and running `which python` on mac/linux or `get-command python` on windows should show you a path to the Python binary inside the env/ directory. Now running pip/python will use the virtualenv PATH/binaries before your global machine PATH. We're ready to install the packages needed for our backend.

#### Install packages listed in requirements.txt
- Run `pip install -r requirements.txt`. This will download any dependencies listed in requirements.txt to your machine (or virtualenv if one is active). After this, you should be ready to run the application.

#### Install PostgresSQL
- Install PostgresSQL on your machine locally. After it's installed, make sure to run the daemon, or run Postgres as a service anytime your machine boots. You'll then need to create a database called `pyStats` and a user/role named `pyStats_user` with a password `pystats` as shown below. After PostgresSQL binaries are on your PATH environment variable, use `psql -U postgres postgres` with password `postgres` to connect to the default table. 
```
DROP DATABASE IF EXISTS "pyStats";
DROP USER IF EXISTS "pyStats_user";
CREATE USER "pyStats_user" WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  CONNECTION LIMIT 1
  PASSWORD 'pystats';
```
- Now we'll create our database and add permissions for our user:
```
CREATE DATABASE "pyStats"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
GRANT ALL ON DATABASE "pyStats" TO "pyStats_user";
```



- IMPORTANT: Don't forget to switch to the new database to create the table in the correct location:
```
\c pyStats
```
- Next, we need to create a new table in Postgres. This SQL will generate the needed table:
```
CREATE TABLE ladder2v2 (
    id SERIAL PRIMARY KEY,
    charName text,
    realm text,
    class text,
    spec text,
    rating integer
);
GRANT ALL ON TABLE public.ladder2v2 TO "pyStats_user";
```

** If you receive a permission denied for sequence error when running the script, you may also have to grant permission for the sequences on Linux versions of postgres by running the following statment**
```
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pyStats_user;
```


#### Test the program
- Run `python main.py`. You should see a browser pop up in the background, and a few new html files (scraping results) should appear in python-stat-tracker/.

