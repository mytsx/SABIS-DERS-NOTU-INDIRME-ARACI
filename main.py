from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
import time
import os
from termcolor import colored
from pyfiglet import Figlet

f = Figlet(font="isometric2")
print(colored(f.renderText("mytsx"), "green"))

print(colored("github: https://github.com/mytsx", "red"))
print(colored("author: Mehmet YERLİ", "red"))


class Sabis():
    def __init__(self, userId, password, driver):
        self.userId = userId
        self.password = password
        self.driver = driver
        # slider ile ayarlattır
        self.delay = 30  # 15 ve 15'in katları olmak zorunda

        options = webdriver.ChromeOptions()
        options.headless = True
        # options.add_argument("--start-maximized")
        p = {"download.default_directory": os.getcwd(),
             "safebrowsing.enabled": "true",
             'excludeSwitches': ['disable-logging']}
        options.add_experimental_option("prefs", p)
        self.browser = webdriver.Chrome(
            self.driver, chrome_options=options)  # "chromedriver.exe"
        self.wait = WebDriverWait(self.browser, self.delay)

    def bul(self, tur, icerik):
        try:
            one = self.wait.until(
                EC.presence_of_element_located((tur, icerik)))
        except TimeoutException:
            print("Loading took too much time!")
        return one

    def siteyeGit(self):
        url = "https://sabis.sakarya.edu.tr/tr/"
        # //*[@id="userid"]
        self.browser.get(url)
        self.browser.maximize_window()
        # time.sleep(1)

    def girisYap(self):
        userId = self.bul(By.ID, "UserName")
        password = self.bul(By.ID, "Password")
        userId.send_keys(self.userId)
        password.send_keys(self.password)
        b1 = self.bul(By.ID, 'btnLogin')
        b1.click()
        time.sleep(2)
        bolmeler = self.browser.find_elements(
            By.XPATH, ".//div[@class='tiles-body']")  # ".//div[@class='tiles-body']"
        bolmeler[1].click()
        username = self.bul(By.ID, "Username")
        pswd = self.bul(By.ID, "Password")
        username.send_keys(self.userId)
        pswd.send_keys(self.password)
        lgnBtn = self.bul(By.XPATH, ".//button[@value='login']")
        lgnBtn.click()
        time.sleep(2)

    def bilgileriGetir(self):
        dersUrl = "https://obs.sabis.sakarya.edu.tr/Ders"
        self.browser.get(dersUrl)
        dersler = self.browser.find_elements(
            By.XPATH, ".//div[@class = 'd-flex flex-row align-items-center py-1']")
        self.dersler = {}
        for ders in dersler:
            id = ders.get_attribute("onclick").split("(")[1].split(")")[0]
            dersUrl = f"https://obs.sabis.sakarya.edu.tr/Ders/Grup/{id}"
            dersAdi = ders.find_element_by_tag_name("a")
            self.dersler[dersAdi.text] = dersUrl, id
        print(self.dersler)

    # dokumanlari ve ders videoları indirmeli
    def dokumanlariIndir(self):
        mainLoc = os.getcwd()
        for dersUrl, id in self.dersler.values():
            # self.browser.get(dersUrl)
            ders = [key for key in self.dersler.keys(
            ) if self.dersler[key] == (dersUrl, id)]
            print(ders)
            time.sleep(2)
            self.browser.get(
                f"https://obs.sabis.sakarya.edu.tr/Ders/Grup/{id}#Dokuman"),
            time.sleep(2)
            div = self.browser.find_element(
                By.XPATH, ".//div[@class='table-responsive']")  # table
            tablo = div.find_element(By.TAG_NAME, "table")
            tbody = tablo.find_element(By.TAG_NAME, "tbody")
            trLer = tbody.find_elements(By.TAG_NAME, "tr")
            syc = 1
            try:
                os.mkdir(ders[0])
            except:
                pass
            os.chdir(os.path.join(mainLoc, ders[0]))
            try:
                os.mkdir("dokumanlar")
            except:
                pass
            os.chdir(os.path.join(os.getcwd(), "dokumanlar"))

            for tr in trLer:
                tds = tr.find_elements(By.TAG_NAME, "td")  # 8 adet td var.
                d = tds[-1].find_element(By.TAG_NAME, "a")
                dosyaTuru = tds[-3].text
                dosyaAdi = tds[1].text
                fileName = f"{syc}_{dosyaAdi}_{dosyaTuru}"
                dersNotuUrl = d.get_attribute("href")
                if dersNotuUrl == f"https://obs.sabis.sakarya.edu.tr/Ders/Grup/{id}#":
                    dersNotuUrl = d.get_attribute("data-video-url")
                print(dersNotuUrl)
                if ("youtu.be" in dersNotuUrl) or ("youtube.com" in dersNotuUrl):
                    f = open(f"{syc}_YOUTUBE_{fileName}.txt", "a+")
                    f.write(dersNotuUrl)
                    f.close()
                else:
                    downloadedFile = self.download_file(dersNotuUrl)
                    os.rename(downloadedFile, fileName)
                    syc += 1
            os.chdir(mainLoc)

    def download_file(self, url):
        local_filename = url.split('/')[-1]
        print("local_filename: ", local_filename)
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        return local_filename
    

    # https://obs.sabis.sakarya.edu.tr/Ders/Grup/657440#Dokuman
    # https://obs.sabis.sakarya.edu.tr/Ders/Grup/657440#SanalSinif


f = open("bilgiler.txt", "r")
bilgiler = [bilgi.replace("\n", "") for bilgi in f.readlines()]
print(bilgiler)

ogNo, pswd = bilgiler

sabis = Sabis(ogNo, pswd, "chromedriver.exe")


sabis.siteyeGit()
sabis.girisYap()
sabis.bilgileriGetir()
sabis.dokumanlariIndir()
