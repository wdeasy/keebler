"""
NowSecure Site - used for testing
"""

from sites.site import Site

class NowSecure(Site):
    """ class for the NowSecure site """

    def login(self, driver):
        print(f'Navigating to {self.name()}.')

        url = 'https://www.nowsecure.nl'

        driver.get(url)

        self.sleep_random(10)


    def config(self, config):
        """ load site configuration """
        if not config.has_section(self.capital_name()):
            config.add_section(self.capital_name())

        if not config.has_option(self.capital_name(), 'enabled'):
            config.set(self.capital_name(), 'enabled', 'True')

        self.enabled = config.getboolean(self.capital_name(), 'enabled')
