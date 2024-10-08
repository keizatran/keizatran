import os
import importlib
from dotenv import load_dotenv
from modules import logger

logger = logger(name='publisher_scraping') # create logger instance

path = os.getcwd()

scraper_folder_name = 'scraper'

scraper_folder_path = path + f'/{scraper_folder_name}/'

os.chdir(scraper_folder_path)

logger.info(f'Initialize scraper ...')

for file in os.listdir():
    if 'init' not in file and 'env' not in file:

        publisher_module = file.replace('.py', '')
        publisher = publisher_module.replace('main_', '').upper()
        scraper = getattr(importlib.import_module(f'{scraper_folder_name}.{publisher_module}'), 'scraper')
        
        logger.info(f'- Start scraping {publisher}')

        #load dynamic variables
        load_dotenv('.publisher_env')
        PROJECT_ID = os.getenv('PROJECT_ID')
        DATASET = os.getenv('DATASET')
        TABLE_NAME = os.getenv(f'{publisher}_TABLE_NAME')
        SERVICE_ACCOUNT = os.getcwd().replace(f'/{scraper_folder_name}','') + '/credential/news-aggregator-1234-dcf71b87711c.json'

        try:
            scraper_instance = scraper(PROJECT_ID, DATASET, TABLE_NAME, SERVICE_ACCOUNT)
            scraper_instance.run()

            logger.info(f'--- Scraped {publisher} done!')
        except Exception as e:
            logger.info(e)
            logger.info(f'--- There was error in excuting code of {publisher}')

logger.info('************* Done *************')