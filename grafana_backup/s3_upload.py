import boto3
from botocore.exceptions import NoCredentialsError


def main(args, settings):
    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    aws_s3_bucket_key = settings.get('AWS_S3_BUCKET_KEY')
    aws_default_region = settings.get('AWS_DEFAULT_REGION')
    aws_access_key_id = settings.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = settings.get('AWS_SECRET_ACCESS_KEY')
    aws_endpoint_url = settings.get('AWS_ENDPOINT_URL')

    backup_dir = settings.get('BACKUP_DIR')
    timestamp = settings.get('TIMESTAMP')

    s3_file_name = '{0}.tar.gz'.format(timestamp)
    archive_file = '{0}/{1}'.format(backup_dir, s3_file_name)

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_default_region
    )

    s3 = session.resource(
        service_name='s3',
        endpoint_url=aws_endpoint_url
    )

    s3_object = s3.Object(aws_s3_bucket_name, '{0}/{1}'.format(aws_s3_bucket_key, s3_file_name))

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
