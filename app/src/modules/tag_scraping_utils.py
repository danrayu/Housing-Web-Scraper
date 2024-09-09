def findElementByString(index, html, searchString, tagType = None): 
  classIndex = html[index:].find(searchString) + index

  current_char = current_char = html[classIndex]
  while current_char != "<" and classIndex - index > 0:
    classIndex = classIndex - 1
    current_char = html[classIndex]
  
  if (classIndex - index < 0):
    return -1
  
  return classIndex

def findTagEnd(index, html):
  if (html[index] != "<"):
    raise ValueError("Character at index must be a tag opening bracket \"<\"")
  
  index = index + 1
  last = len(html) - 1
  currentChar = html[index]
  
  while index <= last and currentChar != ">":
    index += 1
    currentChar = html[index]
    
  if index > last:
    return -1
  
  return index

def extractHref(tag):
  index = tag.find("href")
  
  last = len(tag)-1
  
  parenthesis_count = 0
  begin = 0
  while parenthesis_count < 2 and index <= last:
    if (tag[index] == "\""):
      parenthesis_count += 1
      if parenthesis_count == 1:
        begin = index + 1
    index += 1
  
  if index > last:
    return ""
  
  return tag[begin:index-1]

def confirmIsNew(href, html):
  containerBegin = findElementByString(0, html, href)
  containerEnd = findClosingTag(containerBegin, html)
  isNewMarkerIndex = href[containerBegin:containerEnd].find("MuiChip-root")
  return isNewMarkerIndex != -1
  

def findClosingTag(tagBeginIndex, html):
  if (html[tagBeginIndex] != "<"):
    raise ValueError("Character at index must be a tag opening bracket \"<\"")
  
  index = findTagEnd(tagBeginIndex, html)
  last = len(html) - 1
  depth = 1
  
  while index <= last and depth != 0 and index - tagBeginIndex < 3000:
    index += 1
    currentChar = html[index]
    if currentChar == "<":
      open_index = index
      
      # Scan until the closing of the tag
      while True:
        index += 1
        currentChar = html[index]
        if currentChar == ">":
          is_closing = html[open_index+1] == "/"
          if html[index-1] == "/":
            break
          if html[open_index+1] == "!":
            break
          if is_closing:
            depth -= 1
          else: 
            depth += 1
          break
  if index > last:
    return -1
  
  return index

def findAllHrefs(html, element_match):
  hrefs = []

  cardIndex = findElementByString(0, html, element_match)

  while cardIndex != -1:
    cardTagEnd = findTagEnd(cardIndex, html)
    cardTagClose = findClosingTag(cardIndex, html)
    href = extractHref(html[cardIndex:cardTagEnd+1])
    hrefs.append(href)
    cardIndex = findElementByString(cardTagClose+1, html, element_match)
    
  return hrefs