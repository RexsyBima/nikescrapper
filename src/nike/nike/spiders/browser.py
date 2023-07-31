from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os
from bs4 import BeautifulSoup

class Scroller:
    def __init__(self):
        #wde = WebDriverException
        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        #options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
      
    def scroll(self, url):
        target_url = url
        self.driver.get(target_url)
        print(self.driver.execute_script("return navigator.userAgent"))
        time.sleep(5)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5) # or adjust to a higher value if the page needs longer to load

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def save_html(self, webname):
        time.sleep(10)
        root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        folder_path = os.path.join(root_folder, ".temp","html_output")
        os.makedirs(folder_path, exist_ok=True)
        format_file = os.path.join(folder_path, f"{webname}_NIKE.html")
        with open(format_file, 'w', encoding="utf-8") as f:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            f.writelines(soup.prettify())

    def close(self):
        self.driver.close()
        
    def quit(self):
        self.driver.quit()


"""url = 'https://www.nike.com/id/w/new-womens-3n82yz5e1x6'  # replace with your target URL
    'men_shoes'                   : 'https://www.nike.com/id/w/mens-shoes-nik1zy7ok', v
    'men_clothing'                : 'https://www.nike.com/id/w/mens-clothing-6ymx6znik1', v
    'men_accessories_equipment'   : 'https://www.nike.com/id/w/mens-accessories-equipment-awwpwznik1', v
    'women_shoes'                 : 'https://www.nike.com/id/w/womens-shoes-5e1x6zy7ok', ?? 260 out of 420
    'women_clothing'              : 'https://www.nike.com/id/w/womens-clothing-5e1x6z6ymx6',
    'women_accessories_equipment' : 'https://www.nike.com/id/w/womens-accessories-equipment-5e1x6zawwpw',
    'kids_boys_clothing'          : "https://www.nike.com/id/w/boys-clothing-4413nz6ymx6",
    'kids_boys_shoes'             : "https://www.nike.com/id/w/boys-shoes-4413nzy7ok",
    "kids_girls_clothing"         : "https://www.nike.com/id/w/girls-clothing-6bnmbz6ymx6",
    "kids_girls_shoes"            : "https://www.nike.com/id/w/girls-shoes-6bnmbzy7ok",
    'kids_accessories_equipment'  : 'https://www.nike.com/id/w/kids-accessories-equipment-awwpwzv4dh'
"""
urls = {
       'men_shoes'                   : 'https://www.nike.com/id/w/mens-shoes-nik1zy7ok', #v
    'men_clothing'                : 'https://www.nike.com/id/w/mens-clothing-6ymx6znik1', #v
    'men_accessories_equipment'   : 'https://www.nike.com/id/w/mens-accessories-equipment-awwpwznik1', #v
    'women_shoes'                 : 'https://www.nike.com/id/w/womens-shoes-5e1x6zy7ok', #?? 260 out of 420
    'women_clothing'              : 'https://www.nike.com/id/w/womens-clothing-5e1x6z6ymx6',
    'women_accessories_equipment' : 'https://www.nike.com/id/w/womens-accessories-equipment-5e1x6zawwpw',
    'kids_boys_clothing'          : "https://www.nike.com/id/w/boys-clothing-4413nz6ymx6",
    'kids_boys_shoes'             : "https://www.nike.com/id/w/boys-shoes-4413nzy7ok",
    "kids_girls_clothing"         : "https://www.nike.com/id/w/girls-clothing-6bnmbz6ymx6",
    "kids_girls_shoes"            : "https://www.nike.com/id/w/girls-shoes-6bnmbzy7ok",
    'kids_accessories_equipment'  : 'https://www.nike.com/id/w/kids-accessories-equipment-awwpwzv4dh'
}

if __name__ == "__main__":  
    scroller = Scroller()   
    for webname, url in urls.items():    
        scroller.scroll(url=url)
        scroller.save_html(webname)  # replace 'page.html' with your desired file name     
        print(f"success accessing NIKE {webname} at URL : {url}")
    scroller.quit()
    #scroller.close()
