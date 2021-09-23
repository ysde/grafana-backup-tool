from google import api_core
from google.cloud import storage


def main(args, settings):
    bucket_name = settings.get('GCS_BUCKET_NAME')
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    storage_client = storage.Client()

    gcs_file_name = '{0}.tar.gz'.format(timestamp)
    archive_file = '{0}/{1}'.format(backup_dir, gcs_file_name)

    try:
        bucket = storage_client.get_bucket(bucket_name)

        blob = bucket.blob(gcs_file_name)
        blob.upload_from_filename(archive_file)

        print("Upload to gcs: was successful")
    except FileNotFoundError:  # noqa: F821
        print("The file: {0} was not found".format(gcs_file_name))
        return False
    except api_core.exceptions.Forbidden as e:
        print("Permission denied: {0}, please grant `Storage Admin` to service account you used".format(str(e)))
        return False
    except api_core.exceptions.NotFound:
        print("The gcs bucket: {0} doesn't exist".format(bucket_name))
        return False
    except Exception as e:
        print("Exception: {0}".format(str(e)))
        return False

    return True
