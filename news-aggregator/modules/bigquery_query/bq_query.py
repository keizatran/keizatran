from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from google.oauth2 import service_account

def bq_query(query, service_account_file):
    
    service_account_file = service_account_file

    """ Job to query data from GCP. This job is used to check what the job post ids are already crawled.
    
    Args:
        - query: query
        - project_id: project_id of the data table on GCP.
        - dataset: dataset name on GCP.
        - table_name: table name on GCP; if table already exists, data will be inserted; else create the table and insert data.
        - service_account_file: service account credential to load data to GCP; need to be enabled create permission.
    
    Return: the queried data

    """
    #Auth BQ
    credentials = service_account.Credentials.from_service_account_file(
    service_account_file, scopes=[            
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery"],
    )  
    client = bigquery.Client(credentials=credentials)

    query = query
    
    query_job = client.query(query)
    
    df = query_job.result().to_dataframe()

    return df