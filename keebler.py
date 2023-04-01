"""
Automated cookies.txt generation
"""

import configparser
import http.cookiejar
import json
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from os.path import exists

from sites import instagram
from sites import twitter
from sites import nowsecure

try:
    from selenium.common.exceptions import WebDriverException
except ModuleNotFoundError:
    print('Selenium not installed.')
    print('->  pip install -U selenium')
    sys.exit()

try:
    import undetected_chromedriver as uc
except ModuleNotFoundError:
    print('Undetected Chromedriver not installed.')
    print('->  pip install -U undetected-chromedriver')
    sys.exit()

def get_sites():
    """ list of sites to login """
    sitelist = []

    sitelist.append(instagram.Instagram())
    sitelist.append(twitter.Twitter())
    sitelist.append(nowsecure.NowSecure())

    return sitelist

def get_settings(cfg):
    """ validates the settings section of .kibbler.ini """
    if not cfg.has_section('SETTINGS'):
        cfg.add_section('SETTINGS')

    if not cfg.has_option('SETTINGS', 'headless'):
        cfg.set('SETTINGS', 'headless', 'False')

    if not cfg.has_option('SETTINGS', 'cookies_file'):
        cfg.set('SETTINGS', 'cookies_file', 'cookies.txt')

    if not cfg.has_option('SETTINGS', 'print_user_agent'):
        cfg.set('SETTINGS', 'print_user_agent', 'False')

def check_driver():
    """ Check for new versions of undetected_chromedriver """
    print('Checking for new version of undetected_chromedriver')
    url = 'https://pypi.org/pypi/undetected-chromedriver/json'

    try:
        response = urlopen(url)
    except HTTPError as err:
        print(f'Expected 200 response but received {err.code}')
        return

    data = json.loads(response.read())

    if data is None or data == "":
        print('Version URL response is null or empty.')
        return

    if 'releases' not in data:
        print('No releases found in version data.')
        return

    releases = data['releases']
    if len(list(releases)) < 1:
        print('Release list is empty.')
        return

    remote = list(releases)[-1]
    local = uc.__version__

    remote = remote.lower().strip() if remote is not None else None
    local = local.lower().strip() if remote is not None else None

    if remote != local:
        print(f'Update Available for undetected-chromedriver: {remote}. Current: {local}')
        print('See https://github.com/ultrafunkamsterdam/undetected-chromedriver for details.')
        print('Run "pip install -U undetected-chromedriver" to update.')
        return

    print(f'undetected-chromedriver is to update. {local}')

def get_driver():
    """ create and return a Chromedriver """
    print('Creating Chrome driver.')
    options = uc.ChromeOptions()

    do_headless = config.getboolean('SETTINGS', 'headless')
    if do_headless:
        options.add_argument('--headless')

    try:
        chromedriver = uc.Chrome(options = options)
    except WebDriverException as ex:
        print('Could not create Chrome driver.')
        print(ex)
        sys.exit()()

    print('Created Chrome driver.')
    return chromedriver

def get_config():
    """ load the config file """
    print('Loading Config.')
    config_file = '.keebler.ini'
    cfg = configparser.ConfigParser()

    if exists(config_file):
        cfg.read(config_file)

    get_settings(cfg)

    for site in sites:
        site.config(cfg)

    with open(config_file, 'w', encoding='ascii') as configfile:
        cfg.write(configfile)

    print('Loaded Config.')
    return cfg

def add_cookies(cookie_jar, cookies):
    """ Add chromedriver cookies to an http cookiejar """
    if cookies is None:
        return

    for cookie in cookies:
        cookie_jar.set_cookie(http.cookiejar.Cookie(
        version=0,
        name=cookie['name'] if 'name' in cookie else None,
        value=cookie['value'] if 'value' in cookie else None,
        port='80',
        port_specified=False,
        domain=cookie['domain'] if 'domain' in cookie else None,
        domain_specified=True,
        domain_initial_dot=False,
        path=cookie['path'] if 'path' in cookie else None,
        path_specified=True,
        secure=cookie['secure'] if 'secure' in cookie else None,
        expires=cookie['expiry'] if 'expiry' in cookie else None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None,
        rfc2109=False))

def login_to_sites():
    """ login to each site """
    for site in sites:
        if not site.is_enabled():
            continue

        try:
            site.login(driver)
        except WebDriverException as ex:
            print(f'Error while logging into {site.name()}.')
            print(ex)

def export_cookies():
    """ write cookies to a file """
    print('Exporting Cookies.')

    cookie_jar = http.cookiejar.CookieJar()
    for site in sites:
        add_cookies(cookie_jar, site.get_cookies())

    if len(cookie_jar) < 1:
        print('No Cookies to export.')
        return

    cookies_file = config.get('SETTINGS', 'cookies_file')
    if cookies_file is None or cookies_file == "":
        cookies_file = 'cookies.txt'

    try:
        file = open(cookies_file, 'w', encoding='ascii')
    except FileNotFoundError as err:
        print(f'Could not open {cookies_file} for writing.')
        print(err)

    file.write('# Netscape HTTP Cookie File\n\n')

    for cookie in cookie_jar:
        if cookie.value is None:
            name = ''
            value = cookie.name
        else:
            name = cookie.name
            value = cookie.value

        file.write('\t'.join((
            cookie.domain,
            'TRUE' if cookie.domain.startswith('.') else 'FALSE',
            cookie.path,
            'TRUE' if cookie.secure else 'FALSE',
            '0' if cookie.expires is None else str(cookie.expires),
            name,
            value,
        )) + '\n')

    file.close()
    print(f'Exported Cookies to {cookies_file}')

def do_cleanup():
    """ do closing tasks """
    print_user_agent = config.getboolean('SETTINGS', 'print_user_agent')
    if print_user_agent:
        user_agent = driver.execute_script('return navigator.userAgent')
        print('User Agent:')
        print(user_agent)

    driver.quit()

check_driver()

sites = get_sites()
config = get_config()
driver = get_driver()

login_to_sites()
export_cookies()
do_cleanup()
