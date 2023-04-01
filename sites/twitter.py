"""
Twitter Site
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from sites.site import Site

class Twitter(Site):
    """ class for the Twitter site """    
    def login(self, driver):
        if not self.has_info():
            print(f'Skipping {self.name()}. Missing username or password.')
            return

        print(f'Logging into {self.name()}.')

        url = 'https://twitter.com/login'
        user_element = (By.NAME, 'text')
        pass_element = (By.NAME, 'password')

        driver.get(url)
        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(user_element))
            element.clear()
            element.send_keys(self.username)
            self.sleep_random()
            element.send_keys(Keys.RETURN)
        except TimeoutException:
            print('Timed out waiting on username element.')
            return

        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(pass_element))
            element.clear()
            element.send_keys(self.password)
            self.sleep_random()
            element.send_keys(Keys.RETURN)
        except TimeoutException:
            print('Timed out waiting on password element.')
            return

        try:
            WebDriverWait(driver,10).until(EC.staleness_of(element))
        except TimeoutException:
            print('Timed out waiting on page after login.')
            return

        self.sleep_random(5)

        print(f'Logged into {self.name()}.')
        self.cookies = driver.get_cookies()
