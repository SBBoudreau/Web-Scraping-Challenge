from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)




def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', class_='content_title')
    title1 = title[1].get_text()
    paragraph = soup.find_all('div', class_='article_teaser_body')
    paragraph1 = paragraph[0].get_text()
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)


    browser.click_link_by_partial_text('FULL IMAGE')


    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.select_one('figure.lede a img').get('src')
    print(image)
    image2 = url2 + image
    print(image2)
    url3 = 'https://space-facts.com/mars/'
    df = pd.read_html(url3)[0]
    df
    df.columns = ['Mars Planet Profile', 'Description']
    facts = df.to_html()
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)

    links = browser.links.find_by_partial_text('Hemisphere Enhanced')
    links
    hemispheres = []
    for i in range(len(links)):
        link = browser.links.find_by_partial_text('Hemisphere Enhanced')
        link[i].click()
        sample = browser.links.find_by_partial_text('Sample')[0]
        hemisphere = {}
        hemisphere['image_url'] = sample['href']
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_title = soup.find('h2', class_='title').text
        hemisphere['title']=img_title
        hemispheres.append(hemisphere)
        browser.back()
    hemispheres

    data = {"title": title1, 
            "paragraph": paragraph1,
            "featured_image": image2,
            "Mars_Facts": facts,
            "Hemispheres": hemispheres}
    return data

    
    

