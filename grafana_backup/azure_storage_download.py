from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import io


def main(args, settings):
    arg_archive_file = args.get('<archive_file>', None)

    azure_storage_container_name = settings.get('AZURE_STORAGE_CONTAINER_NAME')
    azure_storage_connection_string = settings.get('AZURE_STORAGE_CONNECTION_STRING')
    
    try:
        if not azure_storage_connection_string:
            print("Azure Storage connection string is not set, using DefaultAzureCredential to authenticate")
            blob_service_client = BlobServiceClient(account_url=settings.get('AZURE_STORAGE_ACCOUNT_URL'), credential=DefaultAzureCredential())
        else: 
            blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
            
        container_client = blob_service_client.get_blob_client(container=azure_storage_container_name, blob=arg_archive_file)
        azure_storage_bytes = container_client.download_blob().readall()
        azure_storage_data = io.BytesIO(azure_storage_bytes)
        print("Download from Azure Storage was successful")
    except Exception as e:
        print(str(e))
        return False

    return azure_storage_data
