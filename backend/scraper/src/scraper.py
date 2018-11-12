#
# src/scraper.py
# 

import os
import sys 
import django

from abc import ABC, abstractmethod
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from api.posts import models

## Utilties 
# Django setup to allow interfacing with django models
def setup_django():
    # Add api to system path to faciliate importing of modules from it
    sys.path.append('api')

    # Django setup to interface with api through django 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.api.settings')
    django.setup()

## Social media model bridges
# Social Media plaforms
class SocialPlatform(Enum):
    Facebook = "facebook"
    Instagram = "instagram"
    Twitter = "twitter"
    
class ContentType(Enum):
    Video = "video"
    Image = "image"

# Represents a form of social content of a certain content type
# Bridges with api's Media model
class SocialContent():
    def __init__(self, content_type, content):
        self.content_type = content_type
        self.content = content
    
    # Commit this object's state to the Media model in the database
    # as the media for the given post object
    def commit(self, post_model):
        # Create media model from object state and assign to post
        model = models.Media.create(kind=self.content_type, src=content)
        post_model.media = model

# Represents a social media posts for a given attributes: 
# platform, author, title, and array of contents
# Bridges with api's Post model
class SocialPost():
    def __init__(platform, author, title, contents=[]):
        self.platform = platform
        self.author = author
        self.title = title
        self.contents = contents
        
    # Commit this object's state to the Post model in the data
    def commit(self):
        # Commit each social content as seperate post models
        for content in contents:
            model = model.Post(author=self.author,
                               platform=self.platform,
                               caption=self.title)
            content.commit(model)
            model.save()

## Social Media Scrapers
# Defines an interface for a Social media scraper that all Social media scrapers 
# will implement
class SocialScraper(ABC):
    @abstractmethod
    # Scrap the given hashtag tag
    # Returns a list of SocialPost posts scraped from the hashtag
    def scrape_hashtag(tag):
        pass

if __name__ == "__main__":
    setup_django()
