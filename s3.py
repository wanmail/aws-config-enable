

def get_s3_policy(bucket_name, accounts):
    """
    Generates an S3 bucket policy for AWS Config service.

    This policy grants AWS Config service permissions to perform specific actions on the specified S3 bucket.

    Refer to https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-policy.html .

    You can setup condition for `aws:SourceOrgID` if you are in an organization environment.

    Args:
        bucket_name (str): The name of the S3 bucket.
        accounts (str): The AWS account ID that owns the bucket.

    Returns:
        dict: A dictionary representing the S3 bucket policy.
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSConfigBucketPermissionsCheck",
                "Effect": "Allow",
                "Principal": {
                    "Service": "config.amazonaws.com"
                },
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Condition": {
                    "StringEquals": {
                        "AWS:SourceAccount": accounts
                    }
                }
            },
            {
                "Sid": "AWSConfigBucketExistenceCheck",
                "Effect": "Allow",
                "Principal": {
                    "Service": "config.amazonaws.com"
                },
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}",
                "Condition": {
                    "StringEquals": {
                        "AWS:SourceAccount": accounts
                    }
                }
            },
            {
                "Sid": "AWSConfigBucketDelivery",
                "Effect": "Allow",
                "Principal": {
                    "Service": "config.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/",

                #   "Resource": "arn:aws:s3:::{s3_bucket_name}/[optional] prefix/AWSLogs/{sourceAccountID}/Config/*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control",
                        "AWS:SourceAccount": accounts
                    }
                }
            }
        ]
    }
