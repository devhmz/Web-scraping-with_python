from utilities import *

from time import time  # Other imports
from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import argparse

parser = argparse.ArgumentParser(description="Linkedin Scraping.")

parser.add_argument(
    "--headless", dest="headless", action="store_true", help="Go headless browsing"
)
parser.set_defaults(headless=False)

parser.add_argument(
    "--download-pfp",
    dest="download_avatars",
    action="store_true",
    help="Download profile pictures of commentors",
)
parser.set_defaults(download_avatars=False)

args = parser.parse_args()

now = datetime.now()
unique_suffix = now.strftime("-%m-%d-%Y--%H-%M")

with open(
    "config.json",
) as f:
    Config = json.load(f)


post_url = check_post_url(Config["post_url"])

##### Writer csv
writer = csv.writer(
    open(
        Config["filename"] + unique_suffix + ".csv",
        "w",
        encoding="utf-8",
    )
)
writer.writerow(["Name", "Headline", "Profile Picture", "Email", "Comment"])

linkedin_username, linkedin_password = login_details()

start = time()  # Starting time
print("Initiating the process....")
##### Selenium Chrome Driver
options = Options()
options.headless = args.headless
driver = webdriver.Chrome(
    options=options, service=Service(ChromeDriverManager().install())
)
driver.get("https://www.linkedin.com")

username = driver.find_element(By.NAME, Config["username_name"])
username.send_keys(linkedin_username)

password = driver.find_element(By.NAME, Config["password_name"])
password.send_keys(linkedin_password)

sign_in_button = driver.find_element(By.XPATH, Config["sign_in_button_xpath"])
sign_in_button.click()

driver.get(post_url)

print("Loading comments :", end=" ", flush=True)
load_more_comments(Config["load_comments_class"], driver)

# comments = driver.find_elements(By.XPATH, '//span[@class="ember-view"]')
# this is bad because in case of comments with mentions or tags, it doesnt work
comments = driver.find_elements(By.CLASS_NAME, Config["comment_class"])
# print(comments)
comments = [comment.text.strip() for comment in comments]

headlines = driver.find_elements(By.CLASS_NAME, Config["headline_class"])
headlines = [headline.text.strip() for headline in headlines]

emails = extract_emails(comments)

names = driver.find_elements(By.CLASS_NAME, Config["name_class"])
names = [name.text.split("\n")[0] for name in names]

avatars = driver.find_elements(By.CLASS_NAME, Config["avatar_class"])


# DEBUGGING
# print(comments[:10])
# print(names[:10])
# print(emails[:10])
# print(avatars[:10])

write_data2csv(names, avatars, headlines, emails, comments, writer)

if args.download_avatars:
    download_avatars(
        avatars, names, Config["dirname"] + unique_suffix
    )

end = time()  # Finishing Time
time_spent = end - start  # Time taken by script

print(
    "%d linkedin post comments scraped in: %.2f minutes (%d seconds)"
    % (len(names), ((time_spent) / 60), (time_spent))
)

driver.quit()
