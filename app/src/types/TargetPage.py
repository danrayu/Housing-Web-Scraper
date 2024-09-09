
class TargetPage:
  def __init__(self, page_url, element_match, request_headers, id):
    self.page_url = page_url
    self.element_match = element_match
    self.request_headers = request_headers
    self.id = id