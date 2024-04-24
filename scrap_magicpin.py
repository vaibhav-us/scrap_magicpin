# Used itertools to iterate over verified proxies from  proxyscrape api

import requests
from bs4 import BeautifulSoup
from itertools import cycle
import time
from selenium import webdriver
import random


def check_proxy(proxy):
    """
    Check if a proxy is working by making a simple HTTP request.
    """
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    target_url = 'https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery/'
    num_pages_to_scrape = 3
    delay_between_requests = 2

    # Fetch proxies separately and store them in a list
    proxies_url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    response = requests.get(proxies_url)
    proxies_list = response.text.splitlines()
    proxies = random.sample(proxies_list, 40)

    verified_proxies = []

    for proxy in proxies:
        if check_proxy(proxy):  
            verified_proxies.append(proxy)
    print(verified_proxies)
    if not verified_proxies:
        return "no verified proxies"

    proxy_pool = cycle(verified_proxies)

    data = []

    for page_number in range(num_pages_to_scrape):
    
        proxy = next(proxy_pool)

        print(f"Using proxy: {proxy}")

   
        

        try:
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument(f'--proxy-server={proxy}')

            # edge_options.add_experimental_option('proxy', proxies_dict)


            driver = webdriver.Edge(options=edge_options)
            driver.get(target_url)

            driver.implicitly_wait(20)
        
            
            input('enter to continue')

            html_t = driver.page_source
            soup = BeautifulSoup(html_t,'lxml')
            data =[]
            
            catalog = soup.find('div', class_='catalogItemsHolder')

            categoryListings= catalog.find_all('article',class_='categoryListing')

            for categoryListing in categoryListings:
    
                card = categoryListing.find_all('section', class_='categoryItemHolder')
    
                for i in card:
                    item_name = i.find('p', class_='itemName').text
                    item_price = i.find('span',class_='itemPrice').text
                    d={
                        "name":item_name,
                        "price":item_price
                    }
                    data.append(d)
    

            print(data) 

            input("exit")

            # Delay between requests to avoid being blocked
            time.sleep(delay_between_requests)
            driver.quit()
        except requests.exceptions.RequestException as e:
            print(f"Error on page {page_number}: {e}")

main()








