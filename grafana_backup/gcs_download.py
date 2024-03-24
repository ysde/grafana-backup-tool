from google import api_core
import io
from google.cloud import storage


def main(args, settings):
    arg_archive_file = args.get('<archive_file>', None)

    bucket_name = settings.get('GCS_BUCKET_NAME')
    bucket_path = settings.get('GCS_BUCKET_PATH').strip('/')

    storage_client = storage.Client()

    gcs_blob_name = arg_archive_file if bucket_path == '' else '{0}/{1}'.format(bucket_path, arg_archive_file)

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(gcs_blob_name)

    try:
        gcs_data = io.BytesIO(blob.download_as_bytes())
        print("Download from GCS: '{0}' was successful".format(bucket_name))
    except FileNotFoundError:  # noqa: F821
        print("The file: {0} was not found".format(arg_archive_file))
        return False
    except api_core.exceptions.Forbidden as e:
        print("Permission denied: {0}, please grant `Storage Admin` to service account you used".format(str(e)))
        return False
    except api_core.exceptions.NotFound:
        print("The file: {0} or gcs bucket: {1} doesn't exist".format(gcs_blob_name, bucket_name))
        return False
    except Exception as e:
        print("Exception: {0}".format(str(e)))
        return False

    return gcs_data
