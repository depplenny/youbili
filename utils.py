import requests, uuid, json

"""
The core operation of the Translator is to translate text. 
from_ is the source language 
to is the target language
key is your  subscription key of Azure Cognitive Services Translator
"""
class Translator:
  def __init__(self, key, from_="en", to="zh-Hans"):
    self.key = key
    self.from_ = from_
    self.to = to


  # This function takes as input a text string
  # and returns a translation string  
  def translate(self, text):
    # Add your subscription key and endpoint
    subscription_key = self.key 
    endpoint = "https://api.cognitive.microsofttranslator.com"
    # Add your location, also known as region. The default is global.
    location = "global"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
      'api-version': '3.0',
      'from': self.from_ ,
      'to': [self.to]
    }

    headers = {
      'Ocp-Apim-Subscription-Key': subscription_key,
      'Ocp-Apim-Subscription-Region': location,
      'Content-type': 'application/json',
      'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
      'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translation = response[0]["translations"][0]["text"]
    
    return translation
  
    







