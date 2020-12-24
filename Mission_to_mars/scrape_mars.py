#importing Dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

def scrape_info():
    browser = init_browser()
    news_title, news_p = mars_news(browser)
    mars_data = {
        title: news_title,
        paragraph: news_p,
        image: featured_image(browser),
        table: mars_facts(),
        hemispheres: hemispheres(browser)
    }
    return mars_data
    
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

def featured_image(browser):
    url1 = 'https://www.jpl.nasa.gov'
    JPLimage_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPLimage_url)
    html = browser.html
    JPLimage_soup = bs(html, "html.parser")
    relative_image_path = JPLimage_soup.find_all('img')[2]["src"]
    featured_url = url1 + relative_image_path
    return featured_url

def mars_facts():
    Mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(Mars_facts_url)
    Mars_facts_df = table[0]
    Mars_facts_df.columns =['Descriptions', 'Values']
    Mars_facts =Mars_facts_df.to_html()
    return Mars_facts

def hemispheres(browser):
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    time.sleep(2)
    hemispheres = []
    links = browser.find_by_css('a.itemLink h3')
    for i in range(len(links)):
 hemisphere = {}
    hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
    browser.find_by_css('a.itemLink h3')[i].click()    
    hemisphere['url'] = browser.links.find_by_partial_text('Sample')['href']
    hemispheres.append(hemisphere)
    browser.back()
    return hemispheres

