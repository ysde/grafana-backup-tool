import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def get_boto_session(settings) -> boto3.Session:
    aws_default_region = settings.get("AWS_DEFAULT_REGION")
    aws_access_key_id = settings.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = settings.get("AWS_SECRET_ACCESS_KEY")

    # If no credentials are provided, boto3 will use the default credentials provider chain.
    if aws_access_key_id is None or aws_secret_access_key is None:
        return boto3.Session(
            region_name=aws_default_region,
        )

    # Otherwise, use the provided credentials.
    return boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_default_region,
    )


def get_s3_resource(settings):
    session = get_boto_session(settings)
    aws_endpoint_url = settings.get("AWS_ENDPOINT_URL")
    s3 = session.resource(
        service_name="s3",
        endpoint_url=aws_endpoint_url,
    )
    return s3


def get_s3_object(settings, s3_file_name):
    aws_s3_bucket_name = settings.get('AWS_S3_BUCKET_NAME')
    aws_s3_bucket_key = settings.get('AWS_S3_BUCKET_KEY')

    s3 = get_s3_resource(settings)
    s3_object = s3.Object(aws_s3_bucket_name,
                          '{0}/{1}'.format(aws_s3_bucket_key, s3_file_name))

    return s3_object
