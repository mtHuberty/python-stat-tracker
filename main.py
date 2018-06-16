from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests as req
import yaml
import sys
import html
import psycopg2

# OPTIONAL - A user can choose a few options by altering values in this file. File is not required for app to run.
def loadConfig():
    with open("config.yml", "r") as stream:
        try:
            cfg = yaml.safe_load(stream)
            print("Config loaded! :\n\t" + str(cfg))
            return cfg
        except yaml.YAMLError as e:
            print("Got a YAML error:\n\t" + str(e))
            return ""

# OPTIONAL - We can hit Blizzard's PvP API for some basic data.
# To toggle this function, comment it out in __main__
def getPvpApiData():
    try:
        return req.get('https://us.api.battle.net/wow/leaderboard/2v2?&locale=en_US&apikey=d6ua4v22fpg2bcqxvspzvf2ncqdsyvgu')
    except req.exceptions.RequestException as e:
        print("Error:\n\t" + str(e) + "\n\tClosing application...")
        sys.exit(1)

# OPTIONAL - We can write the results of the API call from the function above to a json file.
def makeFile(data, fileName="whoops.json"):
    try:
        file = open(fileName, "w")
        file.write(data)
        file.close()
    except IOError as e:
        print("Problem creating pvp-api-data file...\n\t" + str(e) + "\n\tContinuing...")

# Returns a connection to the default database "postgres"
def postgresConnect(host="localhost", dbname="postgres", user="postgres", password=None):
    return psycopg2.connect("host='{}' dbname='{}' user='{}' password={}".format(host, dbname, user, password))

    # TODO - psycopg2 isn't using password at all...strange that it even connects. Need to fix this (with an if password:, else: block)
    # Also, maybe I should find out why the hell it doesn't seem to need a password when I DEFINITELY set one on pgAdmin.





# Here's where all the magic will happen!
if __name__ == "__main__":

    # Open config file and initialize variables from it. No important variables yet.
    cfg = loadConfig()
    pvpApiFile = cfg["filenames"]["pvp-api-file"] + ".json"
    browserType = cfg["browser-type"]

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
    twosBytes = req.get("https://worldofwarcraft.com/en-us/game/pvp/leaderboards/2v2")
    twosText = twosBytes.text
    twosSoup = soup(html.unescape(twosText), "html.parser").encode("utf-8")
    with open("twosSoup.html", "wb") as twosFile: # Note: MUST open file with "wb"(writebytes) as second arg to avoid encoding issues
        twosFile.write(twosSoup)
        twosFile.close()

    # Detect OS of the platform the app is running on and use appropriate chromedriver
    osys = sys.platform
    if osys.startswith("win"):
        print("Windows OS detected...using Windows " + browserType + " driver")
        driverPath = "./browserdrivers/" + browserType + "_drivers/win_" + browserType + "_driver.exe"
    elif osys.startswith("darwin"):
        print("Mac OS detected...using Mac " + browserType + " driver")
        driverPath = "./browserdrivers/" + browserType + "_drivers/mac_" + browserType + "_driver"
    elif osys.startswith("linux"):
        print("Linux OS detected...using Mac " + browserType + " driver")
        driverPath = "./browserdrivers/" + browserType + "_drivers/linux_" + browserType + "_driver"
    else:
        sys.exit("No driver in \"browserdrivers/\" for detected operating system: " + str(osys))

    # This actually DOES work, and the first data we need to save and/or parse is stored in "twosInnerHTML" and then written into "twosInnerHtml.html"
    # Changing the if condition to False will turn off scraping. Data will load from file.
    browser = None
    if True:
        browser = webdriver.Chrome(driverPath)
        browser.get("https://worldofwarcraft.com/en-us/game/pvp/leaderboards/2v2")
        twosInnerHTML = browser.execute_script("return document.body.innerHTML").encode("utf-8")
        with open("twosInnerHtml.html", "wb") as twosInnerHtmlFile:
            twosInnerHtmlFile.write(twosInnerHTML)
            twosInnerHtmlFile.close()
    else:
        with open('twosInnerHtml.html', 'r') as myfile:
            twosInnerHTML = myfile.read().replace('\n', '')
 
    # Open connection and cursor with PostgresSQL instance
    conn = postgresConnect(dbname="pyStats", user="pyStats_user", password="pystats")
    conn.set_session(autocommit=True)
    curs = conn.cursor()

    # Beautiful, BeautifulSoup. I'm bad at this. I don't know what's going on. Trial and error FTW
    twosSoupJs = soup(twosInnerHTML, "html.parser")
    fourBodyDivs = twosSoupJs('div', attrs={'class': 'SortTable-body'})
    targetDiv = fourBodyDivs[4]
    for section in targetDiv:
        charInfoDiv = section.select('div')[1].a.select('div')
        charName = charInfoDiv[11].text
        moreCharInfoList = charInfoDiv[12].text.split(" ")
        charClass = moreCharInfoList[2]
        charSpec = moreCharInfoList[1]
        charPvpDiv = section.select('div')
        charRealm = charPvpDiv[15].text
        charRating = charPvpDiv[20].text
        print(charName + " " + charRealm + " " + charClass + " " + charSpec + " " + charRating)
        sql="""
            INSERT INTO ladder2v2 (charname, realm, class, spec, rating)
                VALUES (%(charName)s, %(realm)s, %(class)s, %(spec)s, %(rating)s)
                ON CONFLICT ON CONSTRAINT unique_char
                DO UPDATE SET spec = %(spec)s, rating = %(rating)s;
            """
        #.format(charName, charRealm, charClass, charSpec, charRating)
        curs.execute(sql, {'charName': charName, 'realm': charRealm, 'class': charClass, 'spec': charSpec, 'rating': charRating})
    curs.close()
    conn.close()
    buttonInner = browser.find_element_by_xpath('//div[@data-text="Next"]')
    buttonInner.send_keys('\n')
    #buttonOuter = buttonInner.find_element(By.XPATH('..'))
    #buttonOuter.click()
    # TODO - Actually parse the interesting stuff
