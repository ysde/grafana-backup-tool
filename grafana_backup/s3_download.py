import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from io import BytesIO

from grafana_backup.s3_common import get_s3_object


def main(args, settings):
    arg_archive_file = args.get("<archive_file>", None)

    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    s3_object = get_s3_object(settings, s3_file_name=arg_archive_file)

    try:
        # .read() left off on purpose, tarfile.open() takes care of that part
        s3_data_raw = s3_object.get()["Body"]
        s3_data = BytesIO(s3_data_raw.read())
        print("Download from S3 was successful")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            print("Error: Key {0} does not exist in bucket {1}".format(
                s3_object.key, aws_s3_bucket_name))
            return False
        raise e
    except NoCredentialsError:
        print("Credentials not available")
        return False

    return s3_data
