import requests
import os
import shutil
import customtkinter as ctk

from PIL import Image
from requests.utils import add_dict_to_cookiejar as ADC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from .. import Parser, string_format

class nHentai:
    def __init__(self, url: str):
        self.BASE_URL = url
        self.session = self.initialize_session()
        
        self.serial = 0
        self.title = []
        self.pages = []
        
    def initialize_session(self):
        session = requests.Session()
        
        data = Parser().read_file()
        header = {
            "User-Agent" : data['nHentai']['User-Agent']
        }
        cookies = {
            "cf_clearance" : data['nHentai']['cf_clearance'],
            "csrftoken" : data['nHentai']['csrftoken']
        }
        
        session.headers.update(header)
        ADC(session.cookies, cookies)
        
        return session
        
    def img2PDF(self, temp_path):
        data = Parser().read_file()
        path = data['UserSetting']['CurrentPath']
        
        images = [
            Image.open(f'{temp_path}/{img}') for img in sorted(os.listdir(temp_path), 
                                                               key = lambda z: int(z.split('.')[0]))]
        images[0].save(f'{path}/{self.serial}.pdf', 
                       "PDF", 
                       resolution = 100.0, 
                       save_all = True, 
                       append_images = images[1:])

    def download_image(self, page_url: str, temp_path: str):
        page_html = self.session.get(page_url).text
        page_soup = BeautifulSoup(page_html, "lxml")

        image_url = page_soup.find("section", id = 'image-container').find('a').find('img')['src']
            
        image_content = requests.get(image_url).content
        image_name = f'{page_url[-1] if page_url[-2] == "/" else page_url[-2:]}.jpg'
                
        with open(f'{temp_path}/{image_name}', "wb") as image_file:
            image_file.write(image_content)
       
    def get_data(self):
        try:
            page_html = self.session.get(self.BASE_URL).text
            page_soup = BeautifulSoup(page_html, "lxml")
            
            info_block = page_soup.find("div", id = 'info')
            pages = info_block.find_all("div", class_ = "tag-container field-name")[-2].find("a").find("span").text
            title = string_format(info_block.find('h1', class_ = 'title').find('span', class_ = 'pretty').text)
            serialid = info_block.find("h3", id = 'gallery_id').text[1:]
            
            self.title.append(title)
            self.pages.extend([''.join([self.BASE_URL, str(page)]) for page in range(1, int(pages) + 1)])
            self.serial += int(serialid)

            return 0
        
        except:
            return 1
        
    def main(self, window):
        index = 1
        data = Parser().read_file()
        
        result = self.get_data()
        
        if result == 0:
            window.insert(f"{index}.end", "Data have been extracted.")
            index += 1
        
        else:
            window.insert(f"{index}.end", "Data extraction aborted.")
            return
        
        temp_path = f"{data['UserSetting']['CurrentPath']}/{self.title[0]}"
        
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
            window.insert(f"{index}.end", "Temporary directory created.")
            index += 1
            
        else:
            window.insert(f"{index}.end", "Directory already exists. Aborted session.")
            index += 1
            return
        
        with ThreadPoolExecutor(max_workers = data['UserSetting']['Parallelism']) as exc:
            futures = [exc.submit(self.download_image, url, temp_path) for url in self.pages]
            [future.result() for future in as_completed(futures)]
        
        window.insert(f"{index}.end", "Pages have been downloaded.")
        index += 1
        
        self.img2PDF(temp_path)
        
        window.insert(f"{index}.end", "Images have been compiled to a PDF.")
        index += 1
        
        shutil.rmtree(temp_path)
        window.insert(f"{index}.end", "Temporary directory has been deleted.")
        index += 1 

        window.insert(f"{index}.end", "Session finished. Download successful.")