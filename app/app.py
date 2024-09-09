from src.modules.tag_scraping_utils import findAllHrefs, confirmIsNew
from src.modules.config_reader import readConfig
from urllib.request import urlopen, Request
from src.data.data_controller import *
from src.types.TargetPage import TargetPage
from src.modules.notifier import *
import time
import re

# read the webpages being scanned into db
config = readConfig("app/config.json")
#config = readConfig("config.json")
print("Adding target pages...")
addTargetPages(config["watched_urls"])
print("Added")

# read them back from the db and loop through em
targetPages: List[TargetPage] = getTargetPages()
for targetPage in targetPages:
  # read html of the site
  request = Request(targetPage.page_url, headers=targetPage.request_headers)
  response = urlopen(request)
  page_html = response.read().decode("utf-8")
  # find the advertisement links
  hrefs = findAllHrefs(page_html, targetPage.element_match)

  # inflate the ads into objects
  adverts = []
  for href in hrefs:
    adverts.append(AdvertType(href, ""))
  
  # fill the db with the initial adverts  
  initAdvertsOfTarget(adverts, targetPage.id)
  print("Added " + str(len(adverts)) + " adverts to the init.")
    
def scan():
  pageAdverts = []
  
  # read them back from the db and loop through em
  targetPages: List[TargetPage] = getTargetPages()
  for targetPage in targetPages:
    # read html of the site
    request = Request(targetPage.page_url, headers=targetPage.request_headers)
    try:
      response = urlopen(request)
    except Exception as e:
      print(f"Exception while getting \"{targetPage.page_url}. Exception message: {e}")
      continue
    page_html = response.read().decode("utf-8")
    # find the advertisement links
    hrefs = findAllHrefs(page_html, targetPage.element_match)

    # inflate the ads into objects
    for href in hrefs:
      advert = AdvertType(href, "")
      isNew = advertIsNew(advert, targetPage.id)
      isNewOrNotKamernet = True
      if targetPage.page_url.find("kamernet.nl") != -1:
        isNewOrNotKamernet = confirmIsNew(href, page_html)
      if isNew and isNewOrNotKamernet:
        addAdvert(advert, targetPage.id)
        pageAdverts.append({"advert": advert, "page": targetPage})
  if len(pageAdverts):
    handleNewAdverts(pageAdverts)
        
def handleNewAdverts(pageAdverts):
  adverts = []
  for padvert in pageAdverts:
    advert = padvert["advert"]
    advert.url = urlFromAdvert(padvert)
    adverts.append(advert)
  notify(adverts, config["recipient_emails"], config["email_credentials"])
    
pattern = re.compile(r'^.+?[^\/:](?=[?\/]|$)')
def urlFromAdvert(pageAdvert):
  page = pageAdvert["page"]
  advert = pageAdvert["advert"]
  base_url_match = pattern.search(page.page_url)
  if base_url_match:
    base_url = base_url_match.group()
    if not base_url.endswith('/'):
      base_url += '/'
    
    advert_url = advert.url.lstrip('/')
    return base_url + advert_url
  else:
    raise ValueError("Could not extract base URL from page URL")
    
  
  
interval = config["interval"] # Number of seconds between each execution

while True:
    scan()
    print("Scanned.")
    time.sleep(interval)