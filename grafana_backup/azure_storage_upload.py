from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential


def main(args, settings):
    azure_storage_container_name = settings.get('AZURE_STORAGE_CONTAINER_NAME')
    azure_storage_connection_string = settings.get('AZURE_STORAGE_CONNECTION_STRING')

    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    azure_file_name = '{0}.tar.gz'.format(timestamp)
    archive_file = '{0}/{1}'.format(backup_dir, azure_file_name)

    try:
        if not azure_storage_connection_string:
            print("Azure Storage connection string is not set, using DefaultAzureCredential to authenticate")
            blob_service_client = BlobServiceClient(account_url=settings.get('AZURE_STORAGE_ACCOUNT_URL'), credential=DefaultAzureCredential())
        else: 
            blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        
        container_client = blob_service_client.get_blob_client(container=azure_storage_container_name, blob=azure_file_name)
        with open(archive_file, 'rb') as data:
            container_client.upload_blob(data)
        print("Upload to Azure Storage was successful")
    except FileNotFoundError:  # noqa: F821
        print("The file was not found")
        return False
    except Exception as e:
        print(str(e))
        return False

    return True
