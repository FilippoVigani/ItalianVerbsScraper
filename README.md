# Italian Verbs Scraper
Python web scraper to get all italian verbs conjugated from the website http://www.italian-verbs.com/.
Used mostly for word games where you need a list of conjugated words locally.

Please use moderately to avoid saturating the server's traffic. You can find a provided output file in this repository as well.

## Usage
Requires `lxml`, `requests` and `progress` modules. Install them accordingly to your operating system, or using `pip install <module_name>`.

Run using python3 (e.g. `python3 scraper.py`. Under Unix and Unix-like systems you can run the script by setting executing permissions `sudo chmod +x scraper.py` and running `./scraper.py` (uses shebang).

The output file will be a .txt file in the same directory of the script containing the list of conjugated verbs (including infinitive verb).
