import boto3
from botocore.exceptions import ClientError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE

from app.core.configs.config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT_URL, S3_BUCKET_NAME


def get_pre_signed_url(object_name: str):
    try:
        s3_client = get_s3_client()

    except Exception as exc:
        # logging.error(exc)
        raise HTTPException(
            status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=f"Error generating app download link"
        )
    else:
        try:
            bucket = S3_BUCKET_NAME
            object_name = object_name

            response = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': object_name
                },
                ExpiresIn=15 * 60
            )
        except ClientError as e:
            # logging.error(e)
            raise HTTPException(
                status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=f"Error generating app download link"
            )


async def get_s3_client() -> boto3:
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )


def get_s3_client_sync() -> boto3:
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )
