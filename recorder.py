

RECORDER_NAME = "default"
DELIVERY_FREQUENCY = "Twelve_Hours"


def get_recoder_config(account_id, region):
    """
    Generates the configuration for AWS Config recorder based on the specified region.
    
    Default excluding `AWS::Config::ResourceCompliance` resource type.

    Parameters:
    account_id (str): The AWS account ID.
    region (str): The AWS region. If the region is "us-east-1", it is considered a global region.

    Returns:
    dict: A dictionary containing the configuration for the AWS Config recorder.
    """
    if region == "us-east-1":
        # global region
        return {
            "name": RECORDER_NAME,
            "roleARN": f"arn:aws:iam::{account_id}:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            "recordingGroup": {
                "allSupported": True,
                "includeGlobalResourceTypes": True,
                "resourceTypes": [],
                "exclusionByResourceTypes": {
                    "resourceTypes": [
                        "AWS::Config::ResourceCompliance"
                    ]
                },
                "recordingStrategy": {
                    "useOnly": "ALL_SUPPORTED_RESOURCE_TYPES"
                }
            },
            "recordingMode": {
                "recordingFrequency": "DAILY",
                "recordingModeOverrides": []
            }
        }
    else:
        return {
            "name": RECORDER_NAME,
            "roleARN": f"arn:aws:iam::{account_id}:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            "recordingGroup": {
                "allSupported": True,
                "includeGlobalResourceTypes": False,
                "resourceTypes": [],
                "exclusionByResourceTypes": {
                    "resourceTypes": [
                        "AWS::Config::ResourceCompliance"
                    ]
                },
                "recordingStrategy": {
                    "useOnly": "ALL_SUPPORTED_RESOURCE_TYPES"
                }
            },
            "recordingMode": {
                "recordingFrequency": "DAILY",
                "recordingModeOverrides": []
            }
        }


def get_delivery_config(bucket_name):
    """
    Generates a configuration dictionary for AWS Config delivery.

    Args:
        bucket_name (str): The name of the S3 bucket where AWS Config will deliver configuration snapshots.

    Returns:
        dict: A dictionary containing the configuration for AWS Config delivery, including the bucket name and delivery frequency.
    """
    return {
        "name": "default",
                "s3BucketName": f"{bucket_name}",
                "configSnapshotDeliveryProperties": {
                    "deliveryFrequency": DELIVERY_FREQUENCY
                }
    }
