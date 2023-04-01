"""
Instagram Site
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from sites.site import Site

class Instagram(Site):
    """ class for the Instagram site """

    def login(self, driver):
        if not self.has_info():
            print(f'Skipping {self.name()}. Missing username or password.')
            return

        print(f'Logging into {self.name()}.')

        url = 'https://www.instagram.com'
        user_element = (By.NAME, 'username')
        pass_element = (By.NAME, 'password')
        login_element = (By.XPATH, '//*[@id="loginForm"]/div/div[3]')
        save_element = (By.XPATH, '//*[ text() = "Not Now" ]')
        notif_element = (By.XPATH, '//*[ text() = "Not Now" ]')

        driver.get(url)
        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(user_element))
            element.clear()
            element.send_keys(self.username)
        except TimeoutException:
            print('Timed out waiting on username element.')
            return

        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(pass_element))
            element.clear()
            element.send_keys(self.password)
        except TimeoutException:
            print('Timed out waiting on password element.')
            return

        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(login_element))
            element.click()
        except TimeoutException:
            print('Timed out waiting on login element.')
            return

        try:
            WebDriverWait(driver,10).until(EC.staleness_of(element))
        except TimeoutException:
            print('Timed out waiting on page after login element.')
            return

        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(save_element))
            element.click()
        except TimeoutException:
            print('Timed out waiting on save element.')
            return

        try:
            WebDriverWait(driver,10).until(EC.staleness_of(element))
        except TimeoutException:
            print('Timed out waiting on page after save element.')

        self.sleep_random()

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(notif_element))
            element.click()
        except TimeoutException:
            print('Timed out waiting on notification element.')
            return

        try:
            WebDriverWait(driver,10).until(EC.staleness_of(element))
        except TimeoutException:
            print('Timed out waiting on page after notification element.')
            return

        self.sleep_random(5)

        print(f'Logged into {self.name()}.')
        self.cookies = driver.get_cookies()
