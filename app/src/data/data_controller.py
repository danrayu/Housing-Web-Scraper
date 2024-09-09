from src.data.peewee_config import *
from src.types.Advert import Advert as AdvertType
from src.types.TargetPage import TargetPage as TargetPageType
from typing import List

db.connect()
db.drop_tables([TargetPage, PageRequestHeader, Advert])
db.create_tables([TargetPage, PageRequestHeader, Advert])

def addTargetPages(pages):
  for page in pages:
    targetPage = TargetPage.create(page_url=page["url"], element_match=page["element_match"])
    for key, value in page["headers"].items():
      targetHeader = PageRequestHeader(header_key=key, header_value=value, page=targetPage)
      targetHeader.save()
    targetPage.save()

def initAdvertsOfTarget(adverts: List[AdvertType], targetPageId):
  targetPage = TargetPage.get(TargetPage.id == targetPageId)
  with db.atomic():
    for advert in adverts:
      Advert.create(url=advert.url, description=advert.description, page=targetPage)

def addAdvert(advert: Advert, targetPageId):
  targetPage = TargetPage.get(TargetPage.id == targetPageId)
  newAdvert = Advert.create(url=advert.url, description=advert.description, page=targetPage)
  newAdvert.save()
  
def advertIsNew(advert: Advert, targetPageId):
  targetPage = TargetPage.get(id=targetPageId)
  targetAdverts = Advert.select().where(Advert.page == targetPage)
  isNew = True
  for existingAd in targetAdverts:
    if existingAd.url == advert.url:
      isNew = False
    
  return isNew

def getTargetPages():
  targetModels = TargetPage.select()
  targetTypes = []
  for model in targetModels:
    targetRequestHeaders = PageRequestHeader.select().where(PageRequestHeader.page == model)
    request_headers = {}
    for header in targetRequestHeaders:
      request_headers[header.header_key] = header.header_value
    targetTypes.append(TargetPageType(model.page_url, model.element_match, request_headers, model.id))
  
  return targetTypes
