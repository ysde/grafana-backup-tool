import boto3
from botocore.exceptions import NoCredentialsError


def main(args, settings):
    arg_archive_file = args.get('<archive_file>', None)

    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    aws_s3_bucket_key = settings.get('AWS_S3_BUCKET_KEY')
    aws_default_region = settings.get('AWS_DEFAULT_REGION')
    aws_access_key_id = settings.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = settings.get('AWS_SECRET_ACCESS_KEY')

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_default_region
    )

    s3 = session.resource('s3')

    s3_object = s3.Object(aws_s3_bucket_name, '{0}/{1}'.format(aws_s3_bucket_key, arg_archive_file))

    try:
        # .read() left off on purpose, tarfile.open() takes care of that part
        s3_data = s3_object.get()['Body']
        print("Download from S3 was successful")
    except NoCredentialsError:
        print("Credentials not available")
        return False

    return s3_data
