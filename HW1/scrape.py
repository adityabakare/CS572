from bs4 import BeautifulSoup
import time
import re
import requests
from random import randint
import urllib.parse
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
SEARCHING_URL = "http://www.search.yahoo.com/search?p="

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: # Prevents loading too many pages too soon
            time.sleep(randint(3, 10))
        temp_url = '+'.join(query.split()) #for adding + between words for the query
        results = []
        count = 0
        page = 1
        while count < 10:
            url = SEARCHING_URL + temp_url + "&b=" + str(page)
            soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
            new_results = SearchEngine.scrape_search_result(soup)
            for result in new_results: # Loop through the new results
                if result not in results: # Check if the result is not duplicated
                    results.append(result) # Add the result to the list
                    count += 1 # Increment the counter
                    if count == 10: # Break the loop if you have 10 results
                        break
            page += 1 # Increment the page number by 1
        return results
    
    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("a", attrs={"class": "d-ib fz-20 lh-26 td-hu tc va-bot mxw-100p"})
        results = []
        for result in raw_results:
            link = SearchEngine.decode_url(result.get('href'))
            print(link)
            results.append(link)
        return results
    
    @staticmethod
    def decode_url(url):
        new_url = urllib.parse.unquote(re.search("RU=(.+?)/RK", url).group(1))
        return new_url
    
class File:
    @staticmethod
    def read_queries(file):
        with open(file, 'r') as f:
            return [line.strip() for line in f.readlines()]
        
    @staticmethod
    def store_results(queries, results, jsonfile):
        data = {}
        for query, result in zip(queries, results):
        # Associate each query with its corresponding result list in the dictionary
            data[query] = result
        with open(jsonfile, "w") as file:
            json.dump(data, file, indent=4)