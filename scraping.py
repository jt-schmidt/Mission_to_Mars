#10.3.3 Scrape Mars Data: The News
# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    #10.3.3 Scrape Mars Data: The News
    # Set the executable path and initialize the chrome browser in splinter
    # Windows users
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres_func(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    #10.3.3 Scrape Mars Data: The News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #10.3.3 Scrape Mars Data: The News
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #10.3.3 Scrape Mars Data: The News
        slide_elem.find("div", class_='content_title')
        #10.3.3 Scrape Mars Data: The News
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #10.3.3 Scrape Mars Data: The News
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

#10.3.4 Scrape Mars Data: Featured Image
# ### Featured Images

def featured_image(browser):

    #10.3.4 Scrape Mars Data: Featured Image
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #10.3.4 Scrape Mars Data: Featured Image
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    #10.3.4 Scrape Mars Data: Featured Image
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    #10.3.4 Scrape Mars Data: Featured Image
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #10.3.4 Scrape Mars Data: Featured Image
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    #10.3.4 Scrape Mars Data: Featured Image
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# 10.3.5 Scrape Mars Data: Mars Facts
def mars_facts():

    try:
        # 10.3.5 Scrape Mars Data: Mars Facts
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    #Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    #Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres_func(browser):
    
    # url = 'https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-earth-k4.html'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    image_urls = []

    html = browser.html
    img_soup = soup(html, 'html.parser')

    first_url = img_soup.find_all("div", class_="item")
    titles = []
    links = []
    hemispheres = []
    dictionary = {}
    root_url = 'https://astrogeology.usgs.gov'

    try:
        for x in first_url:
            titles.append(x.find('h3').text)
            path = x.find("div", class_ = 'description').a['href']
            full_link = root_url + path
            links.append(full_link)

        for y in range(4):
            dictionary = {}
            browser.visit(links[y])
            html = browser.html
            img_soup = soup(html, "html.parser")
            main_url = img_soup.find_all("div", class_="downloads")
            for z in main_url:
                dictionary["title"] = titles[y]
                dictionary["img_url"] = z.find_all("li")[0].a["href"]
            hemispheres.append(dictionary)
    except AttributeError:
        return None

    #full_url1 = f'http://nasa.gov{img_url1}'
    #image_urls = [{title1:full_url1}]
    
    return hemispheres

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())