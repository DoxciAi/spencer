
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from xpaths import XPATHS as xp
from element import Element
import time

# Set up Chrome options
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")

# Specify the path to ChromeDriver executable
service = Service()

# Initialize the driver with the specified options
driver = webdriver.Chrome(service=service, options=options)

class ClickSequence():
    xp=xp
    driver=driver

    def __init__(self, selectors, sleep=0.5):
        self.selectors = selectors
        self.sleep = sleep

    def run(self):
        for i in self.selectors:
            e = Element(driver, i, "XPATH", xp[i])
            e.click()
            time.sleep(self.sleep)



init_seqxp = ["clients",
          "add_client",
          "add_client_client"]



init_seq = ClickSequence(init_seqxp)
time.sleep(3)
init_seq.run()

data = {
    "firstname": "Issac",
    "lastname": "Hicks",
    "dob": "12/02/1994",
    "spousefirstname": "Beyonce",
    "spouselastname": "",
    "spousedob": "01/01/1981",
    "childname": "Blue Ivy",
    "childgender": "Female",
    "child_dob": "01/07/2012",

}

# Existing code to fill out the form for the main client and spouse
firstname = Element(driver, 'add_client_firstname', "XPATH", xp["add_client_firstname"])
firstname.send_keys(data["firstname"])
lastname = Element(driver, 'add_client_lastname', "XPATH", xp["add_client_lastname"])
lastname.send_keys(data["lastname"])
dob = Element(driver, 'add_client_dob', "XPATH", xp["add_client_dob"])
dob.send_keys(data["dob"])

spousefirstname = Element(driver, 'add_client_spouse_firstname', "XPATH", xp["add_client_spouse_firstname"])
spousefirstname.send_keys(data["spousefirstname"])
spouselastname = Element(driver, 'add_client_spouse_lastname', "XPATH", xp["add_client_spouse_lastname"])
spouselastname.send_keys(data["spouselastname"])
spousedob = Element(driver, 'add_client_spouse_dob', "XPATH", xp["add_client_spouse_dob"])
spousedob.send_keys(data["spousedob"])

submit = Element(driver, 'submit', "XPATH", xp["add_client_submit"])
submit.click()

# New code to navigate to the "facts" tab and interact with it
facts = Element(driver, 'facts', "XPATH", xp["facts"])
facts.click()

facts_add = Element(driver, 'facts_add', "XPATH", xp["facts_add"])
facts_add.click()

child = Element(driver, 'child', "XPATH", xp["child"])
child.click()

# Fill out the child's information
childname = Element(driver, 'childname', "XPATH", xp["childname"])
childname.click()
childname.element.clear()
childname.send_keys(data["childname"])


child_dob = Element(driver, 'child_dob', "XPATH", xp["child_dob"])
child_dob.send_keys(data["child_dob"])


gender = Element(driver, 'gender', "XPATH", xp["childgender"])
gender.send_keys(data["childgender"])  

childsave = Element(driver, 'childsave', "XPATH", xp["childsave"])
childsave.click()# Note: This might need to be adjusted if it's a dropdown that requires selecting an option

# Now you can control the existing browser sessionx




