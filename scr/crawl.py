from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep 
from bs4 import BeautifulSoup 
from datetime import datetime 
import requests 
import warnings 
import random 
import json 
warnings.filterwarnings("ignore", category=DeprecationWarning)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Crawler: 

    def __init__(self): 
        chrome_options = Options()
        #chrome_options.add_argument("--headless") #If turn headless on then there is error  
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.articles = [] #url, title, content, created_at
    def crawl(self,url):
        #limit_page = 10 
        unique_urls = set()
        self.driver.get(url)
        sleep(4)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(4)
        view_more_box = self.driver.find_element(By.XPATH, "//*[@id='vnexpress_folder_load_more']")
        for _ in range(4): 
            view_more_box.click()
            sleep(4)
        post_urls = self.driver.find_elements(By.XPATH, "//h2[@class='title_news_site']/a") #If section is perspectives, replace h2 by h4
        #counter = 0 
        for post_url in post_urls: 
            href = post_url.get_attribute("href")
            if href not in unique_urls and "box_comment" not in href: 
                #unique_id = f"hello_{counter}"  # Change for each section 
                #counter += 1 
                unique_urls.add(href)
                #print(href, unique_id)

        self.driver.quit()
        return unique_urls #In set 

    def parse_article(self, url): 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #title = soup.find("h1", class_= "title_post").text.strip()
        #lead_title = soup.find("span", class_= "lead_post_detail row").text.strip()
        try:
            title = soup.find("h1", class_= "title_post").text.strip()
            lead_title = soup.find("span", class_= "lead_post_detail row").text.strip()
            paragraphs = soup.find_all("p", class_ = "Normal") 
            texts = ' '.join([p.text.strip() for p in paragraphs])
            final_text = lead_title + " " + texts
            #print(title)
            #print(final_text)
            #return ((url, title, final_text)) 
            self.articles.append((url, title, final_text,current_time))
        except Exception as e: 
            return "Article not found"
    def main(self): 
        sections = ["news", "business", "travel", "life","sports", "world"]
        base_url = "https://e.vnexpress.net/news/"  #Cant use for because of request limit :))))
        sub_url = random.choice(sections)
        url = base_url + sub_url
        uniqueurls = self.crawl(url)
        for url in uniqueurls: 
            self.parse_article(url)
        #print(f"Crawled{len(self.articles)} articles")
        #print(self.articles[:2])
        return self.articles

if __name__ == "__main__": 
    crawl = Crawler()
    crawl.main()
    articles = crawl.articles
    data = []
    for article in articles: 
        url, title, content, created_at = article
        d = {
            "url": url, 
            "title": title, 
            "content": content, 
            "date": created_at
        }
        data.append(d)
    with open("datasets/news_data.json", "w") as file: 
        json.dump(data, file)













