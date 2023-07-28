from selenium import webdriver
from selenium.common.exceptions import WebDriverException 
import time, os
import platform

class Scroller:
    def __init__(self, url):
        #wde = WebDriverException
        if platform.system() == "Darwin":
            try:
                self.driver = webdriver.Safari()
            except Exception:
                exit()
        else:
            try:
                self.driver = webdriver.Chrome()
            except WebDriverException:
                try:
                    self.driver = webdriver.Firefox()
                except WebDriverException:
                    try:
                        self.driver = webdriver.Edge()
                    except WebDriverException:
                        self.driver = None        
        self.url = url

    def scroll(self):
        self.driver.get(self.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10) # or adjust to a higher value if the page needs longer to load

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
        with open(format_file, 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

    def quit(self):
        self.driver.quit()


#url = 'https://www.nike.com/id/w/new-womens-3n82yz5e1x6'  # replace with your target URL
urls = {
    'men_shoes'                   : 'https://www.nike.com/id/w/mens-shoes-nik1zy7ok',
    'men_clothing'                : 'https://www.nike.com/id/w/mens-clothing-6ymx6znik1',
    'men_accessories_equipment'   : 'https://www.nike.com/id/w/mens-accessories-equipment-awwpwznik1',
    'women_shoes'                 : 'https://www.nike.com/id/w/womens-shoes-5e1x6zy7ok',
    'women_clothing'              : 'https://www.nike.com/id/w/womens-clothing-5e1x6z6ymx6',
    'women_accessories_equipment' : 'https://www.nike.com/id/w/womens-accessories-equipment-5e1x6zawwpw',
    'kids_boys_clothing'          : "https://www.nike.com/id/w/boys-clothing-4413nz6ymx6",
    'kids_boys_shoes'             : "https://www.nike.com/id/w/boys-shoes-4413nzy7ok",
    "kids_girls_clothing"         : "https://www.nike.com/id/w/girls-clothing-6bnmbz6ymx6",
    "kids_girls_shoes"            : "https://www.nike.com/id/w/girls-shoes-6bnmbzy7ok",
    'kids_accessories_equipment'  : 'https://www.nike.com/id/w/kids-accessories-equipment-awwpwzv4dh'
}

if __name__ == "__main__":     
    for webname, url in urls.items():    
        scroller = Scroller(url)
        scroller.scroll()
        scroller.save_html(webname)  # replace 'page.html' with your desired file name
    scroller.quit()
