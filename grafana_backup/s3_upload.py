import boto3
from botocore.exceptions import NoCredentialsError

from grafana_backup.s3_common import get_s3_object


def main(args, settings):
    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    s3_file_name = '{0}.tar.gz'.format(timestamp)
    archive_file = '{0}/{1}'.format(backup_dir, s3_file_name)

    s3_object = get_s3_object(settings, s3_file_name=s3_file_name)

    try:
        s3_object.put(Body=open(archive_file, 'rb'))
        print("Upload to S3 was successful")
    except FileNotFoundError:  # noqa: F821
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

    return True
