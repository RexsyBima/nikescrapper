import scrapy
import os
import subprocess

browse = subprocess.run(['python', 'browser.py'])

def get_html_folder_files():
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
    folder_path = os.path.join(root_folder, ".temp","html_output")
    return folder_path

def get_files_in_folder(folder_path):
    file_list = []

    # List all files and directories in the given folder path
    entries = os.listdir(folder_path)

    for entry in entries:
        # Check if the entry is a file (not a directory)
        if os.path.isfile(os.path.join(folder_path, entry)):
            full_path = os.path.join(folder_path, entry)
            file_list.append("file:\\" + full_path)

    return file_list


class NikespiderSpider(scrapy.Spider):
    name = "nikespider"
    allowed_domains = ["www.nike.com"]
    start_urls = get_files_in_folder(folder_path=get_html_folder_files()) #os.path // path in python

    def parse_price(self, response):
        price = response.css('div.product-price::text').get()
        return price.replace('\xa0', '') #Rp/xa01.500.000 <- -> Rp1.500.000
    
    def parse_colour(self, response):
        colour = response.css('li.description-preview__color-description ::text').get()
        return colour.replace('Colour Shown: ', '')
    
    def parse_img_url(self, response):
        img_url = response.css('img').xpath('@src').getall()
        return img_url[-1]
    
    def parse(self, response):
        products = response.css('div.product-card')
        
        for product in products:
            relative_url = product.css('a.product-card__link-overlay').attrib['href']
            yield response.follow(relative_url, callback=self.parse_product_page)
            
    def product_alternative_product_name(self, response, int_): #fix for https://www.nike.com/id/launch/t/big-kids-air-jordan-6-low-fierce-pink1
        product = response.css('.product-info ::text').getall() 
        if int_ == 2:
            return product[2].replace('\xa0', '')
        elif int_ == 5:
            return response.css('.description-text ::text').get() + '' + product[int_]  
        return product[int_]
            
        #guide : 0 for product title, 1 for color, 2 for price+parse, not yet complete ->3 for category,  5 for description
    
    
    def parse_product_page(self, response):
        product = response.css('body')
        if "/launch/t/" in response.url: # dealing https://www.nike.com/id/launch/t/air-foamposite-one-metallic-red-1
            yield{
            'title'       : self.product_alternative_product_name(response=response, int_=0),
            'category'    : "Launching New Product", #<-- to fix  #product.css('h2.headline-5 ::text').get() or self.product_alternative_product_name(response=response, int_=3)
            'price'       : self.product_alternative_product_name(response=response, int_=2),
            'description' : product.css('.description-text ::text').get(),       #product.css('div.description-preview ::text').get() or self.product_alternative_product_name(response=response, int_=5),
            'colour'      : self.product_alternative_product_name(response=response, int_=1),
            'url'         : response.url, 
            'img_url'     : "None" #<-- to fix #self.parse_img_url(response=response) or self.product_alternative_product_name(response=response, int_=1)                
            }
        else: # dealing https://www.nike.com/id/t/air-pegasus-89-shoes-Jh7lxZ/FN6838-012
            yield{
            'title'       : product.css('h1.headline-2 ::text').get(),
            'category'    : product.css('h2.headline-5 ::text').get(),
            'price'       : self.parse_price(response=response),
            'description' : product.css('div.description-preview ::text').get(),
            'colour'      : self.parse_colour(response=response),
            'url'         : response.url, 
            'img_url'     : self.parse_img_url(response=response)
        }

#poetry - dependensi manager || regex python    \\ dibikin command line \\ typer
#bug products.csv, some link urls doesnt have --> "" <--
