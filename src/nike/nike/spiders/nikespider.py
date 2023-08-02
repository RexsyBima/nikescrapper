import scrapy
import os
import subprocess
import logging

subprocess.run(['python', 'browser.py'])

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
            file_list.append("file://" + full_path)

    return file_list


class NikespiderSpider(scrapy.Spider):
    name = "nikespider"
    allowed_domains = ["www.nike.com"]
    start_urls = get_files_in_folder(folder_path=get_html_folder_files()) #os.path // path in python
    #TO DEAL NORMAL URLs (not launch, and no collection)
    def parse_price(self, response):
        price = response.css('div.product-price::text').get()
        return price.replace('Rp\xa0', '') #Rp/xa01.500.000,00 <- -> 1500000
    
    def parse_colour(self, response):
        colour = response.css('li.description-preview__color-description ::text').get()
        return colour.replace('Colour Shown: ', '')
    
    def parse_img_url(self, response):
        img_url = response.css('img').xpath('@src').getall()
        return img_url[-1]
    #ENDS HERE
#PARSE ALTERNATIVE LINK LAUNCH
    def product_alternative_product_name(self, response, int_): #fix for https://www.nike.com/id/launch/t/big-kids-air-jordan-6-low-fierce-pink1
        product = response.css('.product-info ::text').getall() 
        if int_ == 2:
            return product[2].replace('Rp\xa0', '')
        elif int_ == 5:
            return response.css('.description-text ::text').get() + '' + product[int_]  
        return product[int_]
#PARSE COLLECTION LINKS
    def parse_collection_price(self, response):
        prices = response.css('div.headline-5 ::text').getall()
        new_prices = []
        for price in prices:
            new_prices.append(price.replace('Rp\xa0',''))
        return new_prices
    
    def parse_collection_description(self, response):
        descriptions = response.css('.description-text ::text').getall()
        return [s for s in descriptions if "SKU" not in s]
#PARSING LOOP PROCESS
    def parse(self, response):
        products = response.css('div.product-card')
        for product in products:
            relative_url = product.css('a.product-card__link-overlay').attrib['href']
            yield response.follow(relative_url, callback=self.parse_product_page) #<-- change with scrapy.splash

            
    def parse_product_page(self, response):
        product = response.css('body')
        if "/launch/t/" in response.url and "collection" not in response.url: # dealing #no collection https://www.nike.com/id/launch/t/air-foamposite-one-metallic-red-1 
            image_url_query = self.product_alternative_product_name(response=response, int_=0)
            try:    
                output = {
                'title'       : self.product_alternative_product_name(response=response, int_=0),
                'category'    : "New Product Launch", #<-- to fix  #product.css('h2.headline-5 ::text').get() or self.product_alternative_product_name(response=response, int_=3)
                'price (RP)'  : self.product_alternative_product_name(response=response, int_=2) or "Not Listed",
                'description' : product.css('.description-text ::text').get(),       #product.css('div.description-preview ::text').get() or self.product_alternative_product_name(response=response, int_=5),
                'colour'      : self.product_alternative_product_name(response=response, int_=1),
                'url'         : response.url, 
                'img_url'     : f"https://www.google.com/search?q={image_url_query}&tbm=isch" #<-- to fix #self.parse_img_url(response=response) or self.product_alternative_product_name(response=response, int_=1)                
                }
            except Exception as e:
                self.log('Failed to extract data from: {}'.format(response.url), level=logging.ERROR)
                self.log('Exception message: {}'.format(str(e)), level=logging.ERROR)
                yield output
        elif "/launch/t/" in response.url and "collection" in response.url:
            image_url_query = response.css('div.product-info h1.headline-1 ::text').get() + "" + response.css('div.product-info h5.headline-5 ::text').get()
            try:
                output = {
                'title'       : response.css('div.product-info h2.headline-2 ::text').getall(),
                'category'    : response.css('div.product-info h1.headline-1 ::text').get() + "" + response.css('div.product-info h5.headline-5 ::text').get(), #<-- to fix  #product.css('h2.headline-5 ::text').get() or self.product_alternative_product_name(response=response, int_=3)
                'price (RP)'  : self.parse_collection_price(response=response),
                'description' : self.parse_collection_description(response=response),       #product.css('div.description-preview ::text').get() or self.product_alternative_product_name(response=response, int_=5),
                'colour'      : self.product_alternative_product_name(response=response, int_=1),
                'url'         : response.url, 
                'img_url'     : f"https://www.google.com/search?q={image_url_query}&tbm=isch" #<-- to fix #self.parse_img_url(response=response) or self.product_alternative_product_name(response=response, int_=1)                
                }
            except Exception as e:
                self.log('Failed to extract data from: {}'.format(response.url), level=logging.ERROR)
                self.log('Exception message: {}'.format(str(e)), level=logging.ERROR)
                yield output
        else:
            try:
                output = {
                'title'       : response.css('h1.headline-2 ::text').get(),
                'category'    : response.css('h2.headline-5 ::text').get(),
                'price (RP)'    : self.parse_price(response=response),
                'description' : response.css('div.description-preview ::text').get(),
                'colour'      : self.parse_colour(response=response),
                'url'         : response.url, 
                'img_url'     : self.parse_img_url(response=response)
                }
            except Exception as e:
                self.log('Failed to extract data from: {}'.format(response.url), level=logging.ERROR)
                self.log('Exception message: {}'.format(str(e)), level=logging.ERROR)
            yield output
#poetry - dependensi manager || regex python    \\ dibikin command line \\ typer
#bug products.csv, some link urls doesnt have --> "" <--
# to do use docker+scrapy-splash

