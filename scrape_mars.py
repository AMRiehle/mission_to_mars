import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo

def get_mars_news():
	global news_title, news_p
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	article = soup.find(class_="slide")
	news_title = article.h3.text
	news_p = article.find(class_="article_teaser_body").text

def get_featured_img():
	global mars_featured_img
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)
	mars_img_base_url = 'https://www.jpl.nasa.gov'
	mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(mars_img_url)
	mars_img_html = browser.html
	mars_img_soup = BeautifulSoup(mars_img_html, 'html.parser')
	mars_featured_img = mars_img_base_url + mars_img_soup.find(id='full_image')['data-fancybox-href']

def get_mars_weather():
	global mars_weather
	twitter_url = 'https://twitter.com/marswxreport?lang=en'
	twitter_html = requests.get(twitter_url)
	twitter_soup = BeautifulSoup(twitter_html.text, 'html.parser')
	mars_weather = twitter_soup.find(class_='TweetTextSize--normal').text

def get_mars_facts():
	global df
	df = pd.read_html("https://space-facts.com/mars/")
	df = df[0]
	df.columns = ['description', 'value']
	df = df.set_index('description')
	df.to_html('mars_facts.html')

def get_mars_hemispheres():
	global hemisphere_image_urls
	base_url = 'https://astrogeology.usgs.gov'
	hemisphere1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
	html1 = requests.get(hemisphere1)
	soup1 = BeautifulSoup(html1.text, 'html.parser')
	img1 = base_url + soup1.find_all(class_='wide-image')[0]['src']
	title1 = soup1.find_all(class_='title')[0].text
	hemisphere2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
	html2 = requests.get(hemisphere2)
	soup2 = BeautifulSoup(html2.text, 'html.parser')
	img2 = base_url + soup2.find_all(class_='wide-image')[0]['src']
	title2 = soup2.find_all(class_='title')[0].text
	hemisphere3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
	html3 = requests.get(hemisphere3)
	soup3 = BeautifulSoup(html3.text, 'html.parser')
	img3 = base_url + soup3.find_all(class_='wide-image')[0]['src']
	title3 = soup3.find_all(class_='title')[0].text
	hemisphere4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
	html4 = requests.get(hemisphere4)
	soup4 = BeautifulSoup(html4.text, 'html.parser')
	img4 = base_url + soup4.find_all(class_='wide-image')[0]['src']
	title4 = soup4.find_all(class_='title')[0].text
	hemisphere_image_urls = [
    	{"title": title1, "img_url": img1},
    	{"title": title2, "img_url": img2},
    	{"title": title3, "img_url": img3},
    	{"title": title4, "img_url": img4}
	]

def scrape():
	global mars_dict
	get_mars_news()
	get_featured_img()
	get_mars_weather()
	get_mars_facts()
	get_mars_hemispheres()
	mars_dict = {"news_title": news_title, "news_p": news_p, "mars_featured_img": mars_featured_img, "mars_weather": mars_weather, "mars_hemispheres": hemisphere_image_urls}
	return mars_dict