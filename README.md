# python-stat-tracker
Python web scraper to track WoW PvP stats from the top ranking players in each category.

### Required python packages
For the time being, you may have to figure out which python modules you're missing by trial and error. Try to run the script, it'll error out with ```ModuleNotFoundError: No module named 'bs4'``` 
You'll have to type ```pip install bs4``` and then try again. There aren't too many modules, but I'm going to make a requirements.txt file to make this easier in the near future.

### Note about the chrome driver (in chromedriver_win32)
It's a windows version. That won't work if you're not running on windows, so you'll have to get a different driver and even change the code to reflect the new path to the new driver. It won't be MUCH different, but it certainly won't work unless you do this.
