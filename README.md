
# Keebler

Automated cookies.txt generation using Selenium and undetected_chromedriver. Cookies are exported in Netscape cookie format for use with things like [gallery-dl](https://github.com/mikf/gallery-dl) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).  

## Dependencies

[Chrome](https://www.google.com/chrome/)

[Selenium](https://www.selenium.dev)  

    pip install -U selenium
    
[Undetected Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)  

    pip install -U undetected-chromedriver

## Usage

Do not use with your main accounts or any accounts that you don't want flagged as a bot!

For best results, only run Keebler after your current cookies.txt has expired.

After cloning this repo, run Keebler:

    python keebler.rb

A .keebler.ini file will be created on your first run. Edit this file to add your accounts.

A cookies.txt file will be generated after a successful run.

## Adding New Sites

- Copy an existing site in the sites directory and edit as needed.

- Append your site in the get_sites() function in keebler.py and add it's import.

## Settings

- **headless** - Run Chrome in Headless mode. Headless is **NOT** supported by undetected_chromedriver!

- **cookies_file** - Name of the cookies file to be generated. By default will be in the same directory as the repo.

- **print_user_agent** - Print out the user agent that was used during logins.

- **enabled** - Change enabled to false to skip logging into that site.