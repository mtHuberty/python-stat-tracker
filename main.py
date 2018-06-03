from bs4 import BeautifulSoup as soup
from selenium import webdriver
import requests as req
import yaml
import sys
import html

# Optionally, a user can choose a few options by altering values in this file. File is not required for app to run.
def loadConfig():
    with open("config.yml", "r") as stream:
        try:
            cfg = yaml.safe_load(stream)
            print("Config loaded! :\n\t" + str(cfg))
            return cfg
        except yaml.YAMLError as e:
            print("Got a YAML error:\n\t" + str(e))
            return ""

# Optionally, we can hit Blizzard's PvP API for some basic data.
# To toggle this function, comment it out in __main__
def getPvpApiData():
    try:
        return req.get('https://us.api.battle.net/wow/leaderboard/2v2?&locale=en_US&apikey=d6ua4v22fpg2bcqxvspzvf2ncqdsyvgu')
    except req.exceptions.RequestException as e:
        print("Error:\n\t" + str(e) + "\n\tClosing application...")
        sys.exit(1)

# Optionally, we can write the results of the API call from the function above to a json file.
def makeFile(data, fileName="whoops.json"):
    try:
        file = open(fileName, "w")
        file.write(data)
        file.close()
    except IOError as e:
        print("Problem creating pvp-api-data file...\n\t" + str(e) + "\n\tContinuing...")


# Here's where all the magic will happen!
if __name__ == "__main__":

    # Open config file and initialize variables from it. Not important.
    cfg = loadConfig()
    pvpApiFile = cfg["filenames"]["pvp-api-file"] + ".json"

    # Attempt an HTTP get request to the Blizzard PvP (en_US) API for top player names/classes/specs.
    # TODO - Possibly deprecate this and use scraping only (without calling API)
    dataBytes = getPvpApiData()
    dataText = dataBytes.text
    dataSoup = soup(dataText, "html.parser")

    # Create a file with the data from the API call -- Just because we can. (And for practice with config file etc)
    # makeFile(dataText, pvpApiFile)

    # 2v2 Ladder Scraping.
    # UPDATE: This doesn't work. The data we need is loaded after the DOM is finished loading via javascript probably,
    # so we aren't getting the character names/classes etc.
    twosBytes = req.get("https://worldofwarcraft.com/en-gb/game/pvp/leaderboards/2v2")
    twosText = twosBytes.text
    twosSoup = soup(html.unescape(twosText), "html.parser").encode("utf-8")
    with open("twosSoup.html", "wb") as twosFile: # Note: MUST open file with "wb"(writebytes) as second arg to avoid encoding issues
        twosFile.write(twosSoup)
        twosFile.close()

    # Detect OS of the platform the app is running on and use appropriate chromedriver
    osys = sys.platform
    if osys.startswith("win"):
        print("Windows OS detected...using windows chromedriver")
        driver = "chromedriver.exe"
    elif osys.startswith("darwin"):
        print("Mac OS detected...using Mac chromedriver")
        driver = "mac_chromedriver"
    else:
        sys.exit("No driver in \"chromedrivers/\" for detected operating system: " + str(osys))

    # This actually DOES work, and the first data we need to save and/or parse is stored in "twosInnerHTML" and then written into "twosInnerHtml.html"
    browser = webdriver.Chrome("./chromedrivers/" + driver)
    browser.get("https://worldofwarcraft.com/en-gb/game/pvp/leaderboards/2v2")
    twosInnerHTML = browser.execute_script("return document.body.innerHTML").encode("utf-8")
    with open("twosInnerHtml.html", "wb") as twosInnerHtmlFile:
        twosInnerHtmlFile.write(twosInnerHTML)
        twosInnerHtmlFile.close()

    # TODO - Get BeautifulSoup to use the html file from above (or just use the variable twosInnerHTML), and start parsing it.