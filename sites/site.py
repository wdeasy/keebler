"""
Base site functions
"""

import time
import random

class Site():
    """ base site class with common functions """
    enabled = True
    username = ''
    password = ''
    cookies = None

    def name(self):
        """ site name """
        return self.__class__.__name__

    def capital_name(self):
        """ site name with capitalization """
        return self.name().upper()

    def is_enabled(self):
        """ boolean if the site should be used """
        return self.enabled

    def get_cookies(self):
        """ return cookies for the site """
        return self.cookies

    def has_info(self):
        """ if site has username and password set """
        if self.username is None or self.username == '':
            return False

        if self.password is None or self.password == '':
            return False

        return True

    def login(self, driver):
        """ login steps for the site """
        print(f'No login steps implemented for {self.name()}.')
        print(driver.capabilities['browserVersion'])

    def config(self, config):
        """ load site configuration """
        if not config.has_section(self.capital_name()):
            config.add_section(self.capital_name())

        if not config.has_option(self.capital_name(), 'username'):
            config.set(self.capital_name(), 'username', '')

        if not config.has_option(self.capital_name(), 'password'):
            config.set(self.capital_name(), 'password', '')

        if not config.has_option(self.capital_name(), 'enabled'):
            config.set(self.capital_name(), 'enabled', 'True')

        self.enabled = config.getboolean(self.capital_name(), 'enabled')
        self.username = config.get(self.capital_name(), 'username')
        self.password = config.get(self.capital_name(), 'password')

    def sleep_random(self, loops=1):
        """ sleep a random amount of time  """
        i=0
        while i < loops:
            sec = random.randint(0,1)
            mil = .01 * random.randint(1,59)
            total = sec + mil
            time.sleep(total)
            i+=1
