import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

df = pd.read_csv("/csvfile", sep=';', on_bad_lines='skip')

patents = df['ApplicationId'].tolist() # use patent IDs to form the URLs

def create_urllist(list): # function to create list of patent URLs
    urls = []
    for p in patents:
        url = 'https://patentscope.wipo.int/search/en/detail.jsf?docId=' + p
        urls.append(url)
    return urls

urls = create_urllist(patents)

def create_otherurllist(list): # function to create a list with patentID
    urls = []
    for p in patents:
        url = p + ""
        urls.append(url)
    return urls

patent_numbers = create_otherurllist(patents)

# use Selenium to crawl descriptions from patent dynamic webpages by iterating through URL list
timeout = 5
timeout1 = 10
texts = []

for url, patent_number in zip(urls[0:500], patents[0:500]):
    driver.get(url)
    driver.implicitly_wait(timeout)
    found_element = False
    try:
        desc_button = driver.find_element(By.LINK_TEXT, "Description")
        desc_button.click()
        driver.implicitly_wait(timeout1)
        desc = driver.find_element(By.TAG_NAME, "body")
        description = desc.text
        print("Description found")
        texts.append(description)
        found_element = True  
    except NoSuchElementException: # as not all patents have descriptions available, ignore such patents and keep iterating through the list
        print("Element not found on", url)
        continue
    if found_element: # create a .txt file for each description, using patent ID as file name
        file_name = patent_number + ".txt"
        with open('/txtfiledirectory' + file_name, "w", encoding="utf-8") as f:
            f.write(description)
        continue

print("Done!")
