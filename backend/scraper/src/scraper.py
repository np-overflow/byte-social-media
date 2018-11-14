# -*- coding: utf-8 -*-
#
# src/scraper.py
#

import os
import sys
import django
import re

from abc import ABC, abstractmethod
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool, cpu_count
from time import sleep

# Django setup to allow interfacing with django models
def setup_django():
    # Add api to system path to facilitate importing of modules from it
    sys.path.append('/root/api')

    # Django setup to interface with api through django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    django.setup()

setup_django()  # Must be run before importing models
from posts import models

# Social media model bridges
# Social Media platforms
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
    def __init__(self, content_type, content_url):
        self.content_type = content_type
        self.content_url = content_url

    # Commit this object's state to the Media model in the database
    # as the media for the given post object
    def commit(self, post_model):
        if models.Media.objects.filter(src=self.content_url).exists():
            # Retrieve existing mode from DB if already exists
            model = models.Media.objects.get(src=self.content_url)
        else:
            # Create media model from object state
            model = models.Media.objects.create(kind=self.content_type,
                                                src=self.content_url)

        # Assign model to post
        post_model.media = model

# Represents a social media posts for a given attributes:
# platform, author, caption, and array of contents
# Bridges with api's Post model
class SocialPost():
    def __init__(self, platform, post_id, author, caption, contents=[]):
        self.platform = platform
        self.post_id = post_id
        self.author = self.truncate_str(author, 100)
        self.caption = self.truncate_str(caption, 400)
        self.contents = contents

    @staticmethod
    def truncate_str(s, max_length):
        if len(s) > max_length:
            # Add elipsis character if it is too long
            return s[:max_length-1] + "…"
        else:
            return s

    # Commit this object's state to the Post model in the data
    def commit(self):
        # Only commit the model if it doesn't already exists in DB
        if not models.Post.objects.filter(post_identifier=self.post_id).exists():
            # Create separate post models for each piece of content
            for content in self.contents:
                model = models.Post.objects.create(author=self.author,
                                                   platform=self.platform,
                                                   caption=self.caption)
                content.commit(model)
                model.save()

## Social Media Scrapers
# Defines an interface for a Social media scraper that all Social media scrapers
# will implement
class SocialScraper(ABC):
    def __init__(self):
        # Setup web scraper driver
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        self.driver.implicitly_wait(5)  # wait for 5 sec when trying to find elements

    def close(self):
        self.driver.close()

    ## Scraper Utilities
    # Scroll to the bottom of the page
    def scroll_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    # Navigate back through history using JS
    def navigate_back(self):
        self.driver.execute_script("window.history.go(-1)")

    # Perform search of given search term on social media website
    @abstractmethod
    def search(self, term):
        pass

    @abstractmethod
    # Scrape the given hashtag tag
    # Returns a list of SocialPost posts scraped from the hashtag
    def scrape_hashtag(self, tag):
        pass

# Create Social Media Scraper that targets Instagram
class InstagramScraper(SocialScraper):
    def __init__(self):
        super().__init__()
        self.login()

    ## Scraper Actions
    # Perform instagram login using credentials from the env vars
    # INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD
    def login(self):
        # Retrieve login page and extract elements
        self.driver.get("https://www.instagram.com/accounts/login/")
        username_input = self.driver.find_element_by_name("username")
        password_input = self.driver.find_element_by_name("password")
        login_button = \
            self.driver.find_element_by_css_selector('button[type="submit"]')

        # Enter credentials
        username_input.send_keys(os.environ["INSTAGRAM_USERNAME"])
        password_input.send_keys(os.environ["INSTAGRAM_PASSWORD"])

        # Perform login
        login_button.click()

    # Perform search of given search term on instagram
    # Returns True if search is performed successfully otherwise False
    def search(self, term):
        # Retrieve search bar element
        search_input = self.driver.\
            find_element_by_css_selector('input[type="text"][placeholder="Search"]')
        # Input search term
        search_input.send_keys(term)
        # Wait for search results
        self.driver.find_element_by_xpath("//nav/div[2]/"
                                          "div/div/div[2]/div[2]/div[2]")

        n_results = len(self.driver.find_elements_by_xpath(
            "//nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a"))
        if n_results > 0:
            # Perform search
            search_input.send_keys(Keys.ENTER)
            search_input.send_keys(Keys.ENTER)
            return True
        else:
            return False

    # Extract post urls from the specified number of pages n_page
    # Returns a list of extracted urls
    def extract_urls(self, n_page):
        post_urls = set()

        for i in range(n_page):
            # Retrieve posts elements
            post_anchors = self.driver.find_elements_by_xpath("//article//a")

            # Collate posts urls
            for anchor in post_anchors:
                post_url = anchor.get_attribute("href")
                post_urls.add(post_url)

            # Scroll to obtain new page of posts
            self.scroll_bottom()
            sleep(0.5)

        return list(post_urls)

    # Process post infomation from the post specified by the given post_url
    # Embeds post infomation in a SocialPost
    # Returns the SocialPost
    def process_post(self, post_url):
        # Retrieve post elements
        self.driver.get(post_url)

        # Extract post id from url
        post_id = re.search("/([a-zA-Z0-9]+)/?", post_url).group(1)

        # Extract post author
        # NOTE: Does not always work
        author_element =  \
            self.driver.find_element_by_xpath(
                "//article/header/div[2]/div[1]/div[1]/h2/a")
        author = author_element.text

        # Extract post caption
        caption_element = \
            self.driver.find_element_by_xpath(
                "//article/div[2]/div[1]/ul/li[1]/div/div/div/span")
        caption = caption_element.text

        # Extract post content(s)
        contents = []
        # Extract SocialContent from content element
        def extract_content(element):
            has_img = len(element.find_elements_by_tag_name("video")) == 0

            content_type = ContentType.Image.value if has_img else ContentType.Video.value
            if has_img:
                content = element.find_element_by_tag_name("img")
            else:
                content = element.find_element_by_tag_name("video")
            content_url = content.get_attribute("src")

            return SocialContent(content_type,
                                 content_url)


        content_div = \
            self.driver.find_element_by_xpath("//article/div[1]")

        # Determine if multiple images has to be extracted from a carousel
        has_carousel = len(content_div.find_elements_by_tag_name("ul")) != 0

        if has_carousel:
            # Extract multiple content elements from carousel
            for content_wrapper in content_div.find_elements_by_xpath(
                    "div/div/div/div[2]/div/div[1]/div/ul/li"):

                next_button = content_div.find_elements_by_xpath(
                    "div/div/div/div[2]/button")[-1]

                # Extract content element
                content_element = content_wrapper.find_element_by_xpath(
                    "div/div/div/div[1]")
                content = extract_content(content_element)
                contents.append(content)

                next_button.click()
        else:
            # Extract single content element
            content_element = content_div.find_element_by_xpath("div/div[1]/div[1]")
            content = extract_content(content_element)
            contents.append(content)

        # Construct SocialPost from extracted content
        return SocialPost(post_id=post_id,
                          platform=SocialPlatform.Instagram.value,
                          author=author,
                          caption=caption,
                          contents=contents)

    # Scrape the given hastag on instagram
    # Returns a list of parsed SocialPost from the given hashtag
    def scrape_hashtag(self, tag):
        has_results = self.search(tag)

        if has_results:
            sleep(2)  # wait for the search to load
            post_urls = self.extract_urls(n_page=1)
            posts = list(map(self.process_post, post_urls))
        else: posts = []

        # reset page
        self.driver.get("https://www.instagram.com")

        return posts


if __name__ == "__main__":
    while True:
        scraper = None
        try:
            scraper = InstagramScraper()
            # Scrape the hashtag
            hashtags = ["#bytehackz", "#bytehackz2018", "#bytehackzhackathon"]
            for hashtag in hashtags:
                print("Scrapping {} hashtag...".format(hashtag))
                posts = scraper.scrape_hashtag(hashtag)
                print("scraped {} posts for {}".format(len(posts), hashtag))
                print("Commiting to DB...")
                for p in posts:
                    p.commit()
        except Exception as e:
            print(e)
        finally:
            if scraper is not None:
                scraper.close()
