from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from tqdm import tqdm

from modules import bq_load, bq_query

class scraper():

    def __init__(self, PROJECT_ID, DATASET, TABLE_NAME, SERVICE_ACCOUNT):
        self.url = 'https://www.engadget.com'

        self.project_id = PROJECT_ID
        self.dataset = DATASET
        self.table_name = TABLE_NAME
        self.service_account = SERVICE_ACCOUNT

        self.data_dict = {
            'title': [],
            'sub_title': [],
            'body': [],
            'keyword': [],
            'link': [],
            'id': [],
            'date_published': [],
            'date_modified': [],
            'publisher': [],
            'publisher_link': [],
            'author_name': [],
            'author_title': [],
            'image_url': [],
            'video_url': [],
        }

    def make_request(self, url):
        response = requests.get(url)

        if response.ok:
            try:
                soup = BeautifulSoup(response.text, 'lxml')
                return soup
            except Exception:
                print('There was error in data extraction!')
                return None
        else:
            print('There was error in requests!')
            return None
    
    def extract_article_url(self, url):
        
        soup = self.make_request(url)

        try:
            articles = soup.find('div', id='module-latest').find_all('article', attrs={'data-component':'PostCard'})
        except:
            articles = soup.find('main', attrs={'class':'W(100%)', 'role' :'main'}).find_all('article', attrs={'data-component':'PostCard'})

        def extract_post_id(link):
            # Find one or more digits (\d+) at the end of the string ($)
            matches = re.finditer(r'\d+', link)
            extracted_numbers = [match.group() for match in matches]
            try:
                id = extracted_numbers[len(extracted_numbers)-1]
                return id
            except:
                return None

        self.data_dict['link'].extend(['https://www.engadget.com/' + article.div.a['href'] if article.div.a['href'] else None for article in articles])
        self.data_dict['id'].extend([extract_post_id(article.div.a['href']) if article.div.a['href'] else None for article in articles])
        self.data_dict['title'].extend([article.div.a['title'] if article.div.a['title'] else None for article in articles])
    
    def extract_article_information(self, url):
        soup = self.make_request(url)

        article = soup.find('div', id='caas-content-body').find('article', attrs={'role':'article'})
        schema = json.loads(article.find('script', type="application/ld+json").text)
        
        self.data_dict['sub_title'].append(article.find('div', class_='caas-content-wrapper').find('h2').text if article.find('div', class_='caas-content-wrapper').find('h2') else None)
        self.data_dict['body'].append(article.find('div', class_='caas-body').text if article.find('div', class_='caas-body') else None)
        self.data_dict['keyword'].append(schema['keywords'])
        self.data_dict['date_published'].append(schema['datePublished'])
        self.data_dict['date_modified'].append(schema['dateModified'])
        self.data_dict['author_name'].append(schema['author']['name'])
        self.data_dict['author_title'].append(schema['author']['jobTitle'])
        self.data_dict['publisher'].append(schema['publisher']['name'])
        self.data_dict['publisher_link'].append(schema['publisher']['url'])     
        self.data_dict['image_url'].append(article.find('div', class_='caas-img-container').find('img', src=True)['src'] if article.find('div', class_='caas-img-container') is not None and article.find('div', class_='caas-img-container').find('img', src=True) is not None else None)
        self.data_dict['video_url'].append(article.find('div', class_='caas-iframe-wrapper').find('iframe', src=True)['src'] if article.find('div', class_='caas-iframe-wrapper') is not None and article.find('div', class_='caas-iframe-wrapper').find('iframe', src=True) is not None else None)

    def scraper(self):
        for page in tqdm(range(1, 4), desc='Scraping pages ...'): # can only access 200 pages on Homepage. Extract first 3 pages and compare with data on dwh
            self.extract_article_url(url=f'{self.url}/page/{page}') # extract article url on the each page 1 of Homepage

        # loop thru each article url and extract data
        for url in tqdm(self.data_dict['link'], desc='Scraping posts ...'):
            self.extract_article_information(url=url) 
        
        df = pd.DataFrame.from_dict(self.data_dict)

        # query data from DWH
        QUERY = f"""
        SELECT DISTINCT id FROM `{self.project_id}.{self.dataset}.{self.table_name}`
        """

        df_existing_id = bq_query(query=QUERY, service_account_file=self.service_account)

        df_new_posts = df[df['id'].astype(str).isin(df_existing_id['id'].astype(str))==False]
        
        return df_new_posts
    
    def run(self):
        df_new_posts = self.scraper()
        new_posts = int(df_new_posts['id'].nunique())

        if new_posts > 0:

            load_job = bq_load(df=df_new_posts, project_id=self.project_id, dataset=self.dataset, table_name=self.table_name, service_account_file=self.service_account)

            if load_job == True:
                print(f'Upload {new_posts} new posts successfully')
            else:
                print('There was error in load job')
        
        else:
            print('No new job posts')