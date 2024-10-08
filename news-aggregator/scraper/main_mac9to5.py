from curl_cffi import requests
from pandas import json_normalize
from modules import clean_html, convert_to_utf8, bq_query, bq_load

import pandas as pd
import time


class scraper:
    def __init__(self, PROJECT_ID, DATASET, TABLE_NAME, SERVICE_ACCOUNT):
        self.project_id = PROJECT_ID
        self.dataset = DATASET
        self.table_name = TABLE_NAME
        self.service_account = SERVICE_ACCOUNT

        self.url = "https://9to5mac.com/wp-json/wp/v2/posts?"

        self.params = {
            "per_page": 100,
            "order": "desc",
            "orderby": "date",
        }

        self.page_num = 1

        self.cols = {
            "id": "post_id",
            "title.document_title": "post_title",
            "link": "post_link",
            "yoast_head_json.article_published_time": "date_published",
            "yoast_head_json.article_modified_time": "date_modified",
            "yoast_head_json.og_description": "post_description",  # fully filled
            "yoast_head_json.og_site_name": "publisher_name",
            "author": "author_id",
            "yoast_head_json.author": "author_name",
            "parsely.meta.articleSection": "category",  # need to find further
            "content.rendered": "post_content",  # use regexp to retrieve all the link in html code => media
            "yoast_head_json.schema.@graph": "schema_graph",  # unnest to find word count, cmt count
        }

    def get_url(self, url: str, **params: dict) -> str:
        """
        Functions to get url & parameters.

        Args:
            - url: website domain
            - params: dictionary contains url query parameters

        Return: url with parsed parameters
        """

        string = ""
        for key, value in params.items():
            string += f"{key}={value}&"

        request_url = url + string[:-1]
        return request_url

    def make_request(self, request_url: str):
        response = requests.get(request_url)
        if response.ok:  # True

            try:
                data = response.json()
                return data

            except:
                print("There was error in data extraction!")
                return None

        else:
            print("There was error in requests!")
            return None

    def extract_data(self, data: dict, cols: dict):

        if data:

            df = pd.DataFrame(json_normalize(data))[
                cols.keys()
            ]  # convert to df and filter columns

            df.columns = cols.values()  # rename columns

            return df

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:

        data["post_content"] = (
            data["post_content"].apply(clean_html).apply(convert_to_utf8)
        )
        data["post_description"] = data["post_description"].apply(convert_to_utf8)
        data["schema_graph"] = data["schema_graph"].astype(str)
        return data

    def data_extract(self):
        df = pd.DataFrame({})
        total_time = 0

        page_num = self.page_num

        while page_num <= 5:

            start_time = time.time()
            print(f"Scraping Page {page_num}...")

            try:
                data = self.transform_data(
                    self.extract_data(
                        self.make_request(
                            self.get_url(self.url, page=page_num, **self.params)
                        ),
                        self.cols,
                    )
                )
                # query data from DWH
                QUERY = f"""
                SELECT DISTINCT post_id FROM `{self.project_id}.{self.dataset}.{self.table_name}`
                """

                df_existing_id = bq_query(
                    query=QUERY, service_account_file=self.service_account
                )

                df_new_posts = data[
                    data["post_id"].astype(str).isin(df_existing_id["post_id"]) == False
                ]

                df = pd.concat([df, df_new_posts], ignore_index=True)

            except Exception as err:
                print(f"Scraping Error: {err}")

            time.sleep(1)
            end_time = time.time()  # End time of the iteration
            execution_time = end_time - start_time  # Calculate execution time

            print(
                f"Done Scraping Page {page_num}: Execution time = {execution_time:.2f} seconds"
            )

            page_num += 1
            total_time += execution_time

            print(f"Total Accumulated time = {total_time:.2f} seconds \n")

        return df

    def run(self):
        df = self.data_extract()
        try:
            bq_load(
                df,
                self.project_id,
                self.dataset,
                self.table_name,
                self.service_account,
            )
            if bq_load:
                print("Done Uploading")
        except Exception as err:
            print(f"Load Error: {err}")
