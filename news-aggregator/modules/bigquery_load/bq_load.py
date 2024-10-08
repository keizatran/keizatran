from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from google.oauth2 import service_account

def bq_load(df, project_id, dataset, table_name, service_account_file) -> bool:
    
    """ Job to load data from local to GCP.
    
    Args:
        - df: the dataframe in tabular format.
        - project_id: project_id of the data table on GCP.
        - dataset: dataset name on GCP.
        - table_name: table name on GCP; if table already exists, data will be inserted; else create the table and insert data.
        - service_account_file: service account credential to load data to GCP; need to be enabled create permission.
    
    Return: Result of the job

    """
    #Auth BQ
    credentials = service_account.Credentials.from_service_account_file(
    service_account_file, scopes=[            
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery"],
    )  
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    project_id = project_id

    # The schema of df must match the schema of the table
    table_id = project_id + "." + dataset + "." + table_name
    job_config = bigquery.LoadJobConfig(
        # use WRITE_TRUNCATE if you want to replace the table with the newly data
        # if not, the new data will be appended to the table
        # write_disposition="WRITE_TRUNCATE",
        autodetect=True
        )
    try:
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )  # Make an API request.
        job.result()  # Wait for the job to complete.

        data_rows = df.shape[0]
        data_columns = df.shape[1]

        # table = client.get_table(table_id)  # Make an API request.

        return True
    except:
        return False