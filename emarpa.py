# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Process audio file
from icecream import ic
import symbl
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from element import Element
import selenium

from datetime import datetime, timedelta
import time
import code
import pyaudio
import wave


    
options = webdriver.ChromeOptions()
# options.add_argument('--disable-http2')
# options.add_argument('--enable-logging')
# options.add_argument('--v=1')


# options = FirefoxOptions()


# service = FirefoxService(executable_path='./geckodriver')
# options.set_capability("acceptInsecureCerts", True) # Accept insecure certificates
# options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
# options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
# options.add_argument("--disable-extensions")  # Disable extensions
# options.add_argument("--no-sandbox")
# driver = webdriver.Firefox(service=service, options=options)
# driver.get("https://wealth.emaplan.com/ema/SignIn?ema%2Fria%2Fgauta")


service = webdriver.chrome.service.Service(log_path='/dev/null')
driver = webdriver.Chrome(options=options, service=service)
driver.get("https://wealth.emaplan.com/ema/SignIn?ema%2Fria%2Fgauta")



username = Element(driver, "username", "XPATH", "/html/body/div/div[1]/div/div[2]/div/form/div[1]/input")
username.send_keys("SpencerGauta")
next = Element(driver, "username", "XPATH", "/html/body/div/div[1]/div/div[2]/div/form/button")
next.click()
input()

