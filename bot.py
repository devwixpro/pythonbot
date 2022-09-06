import time
import json
import shutil
import os
from selenium.webdriver.common.by import By

USER_DATA_DIR = "userData"
COOKIES_DIR = "cookeis"
NUMBER_OF_PROFILES = 1
def removeProfiles(): 
    try:
        shutil.rmtree(USER_DATA_DIR)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def makeProfiles():
    profilePaths = []
    for i in range(NUMBER_OF_PROFILES):
        if not os.path.exists(f'{USER_DATA_DIR}/user-{i}'):
            os.makedirs(f'{USER_DATA_DIR}/user-{i}')
            profilePaths.append(f'{USER_DATA_DIR}/user-{i}')
    return profilePaths

def myfunc(cookieFb):
    cookieFb['sameSite'] = 'Lax'
    return cookieFb

def readCookies():
    cookieFiles = os.listdir(COOKIES_DIR)
    cookies = []
    for cookieFile in cookieFiles:
        with open(f'{COOKIES_DIR}/{cookieFile}', 'r', newline='') as json_file:
           cookie = json.load(json_file)
           cookiesData = cookie["cookies"]
           mappedCookie = map(myfunc, cookiesData)
           cookies.append(mappedCookie)
    return cookies

def main (): 
    removeProfiles()
    profilePaths = makeProfiles()
    for index, profilePath in enumerate(profilePaths):
        import undetected_chromedriver as uc
        options = uc.ChromeOptions()
        options.user_data_dir = f'{profilePath}'
        options.headless=False
        chrome = uc.Chrome(options=options)
        cookeis = readCookies()
        chrome.delete_all_cookies()
        chrome.set_page_load_timeout(120)
        chrome.get('https://www.facebook.com')
        for cookie in cookeis[index]:
            chrome.add_cookie(cookie)
        chrome.get('https://vidtrickssl.blogspot.com/2022/08/testing-1.html')
        chrome.refresh()
        chrome.refresh()
        time.sleep(60)
        elements = chrome.find_elements(By.CSS_SELECTOR, "div>span>iframe")
        for element in elements:
            element.click()
        time.sleep(900)
        chrome.save_screenshot('datadome_undetected_webddriver.png')

if __name__=="__main__":
    main()

