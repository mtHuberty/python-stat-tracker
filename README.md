# python-stat-tracker
Python web scraper to track WoW PvP stats from the top ranking players in each category. Currently, only a backend web-scraping portion is under construction. A frontend and possibly discord bot will be built to display the data in the near future!

### Note about the browser drivers (in /chromedrivers/)
Currently, both Mac and Windows drivers are in the folder and the python script will detect which environment it's running on and use the appropriate driver, so it should work out of the box on Mac/Windows. Linux support coming soon (before we move it to centOS).

---

### Getting started with development

#### Get virtualenv
It's highly recommended to use virtualenv to manage your python packages. Assuming you already have python3.4+ and pip, and have cloned this repo:
- Make sure pip is tied the correct version of Python (3.4+) by typing `pip --version` in your console. If it's not, you may need to use pip3 or reintall python or pip.
- `pip install virtualenv` (or `pip install virtualenv --user` on a Mac)
- `cd` into the python-stat-tracker directory
- `virtualenv env` - This will create a new virtual environment in a folder called "env", along with whichever python version installed the virtualenv package. 
- This next part depends on your OS
  - For windows, (on powershell), Run `.\env\bin\activate`. If you get permission problems, first run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` and choose "Yes to All". This should let you execute the activate script.
  - For Mac, Run `source env/bin/activate`
- You should see (env) at the beginning of your shell prompt now, and running `which python` on mac/linux or `get-command python` on windows should show you a path to the Python binary inside the env/ directory. Now running pip/python will use the virtualenv PATH/binaries before your global machine PATH. We're ready to install the packages needed for our backend.

#### Install packages listed in requirements.txt
- Run `pip install -r requirements.txt`. This will download any dependencies listed in requirements.txt to your virtualenv. After this, you should be ready to run the application.

#### Test the program
- Run `python main.py`. You should see a browser pop up in the background, and a few new html files (scraping results) should appear in python-stat-tracker/.
