# aws-config-enable
Enable AWS Config configuration in multiple accounts and regions.

### Prerequisite
```
pip install boto3
```

### Change Your Configuration
Setup your `sso portal`、`sso rolename`、`delivery bucket name` in main.py.

For example
```python
SSO_LOGIN_URL = 'https://example.awsapps.com/start/#'
ROLE_NAME = 'SecurityAudit'

BUCKET_NAME = 'config-bucket-example'
```

You can also change to aws profile for authentication.

### Process
#### SSO Login
```bash
aws sso login
```

#### execute
```bash
python main.py
```

#### SSO Logout
```
aws sso logout
```

### Setup S3 Policy
After executing this script, screen will output a policy configuration for your S3 bucket.
Apply the policy configuration, so that every account can put configuration records to the bucket.

Such as the following:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSConfigBucketPermissionsCheck",
      "Effect": "Allow",
      "Principal": {
        "Service": "config.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::amzn-s3-demo-bucket",
      "Condition": { 
        "StringEquals": {
          "AWS:SourceAccount": "sourceAccountID"
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
      "Resource": "arn:aws:s3:::amzn-s3-demo-bucket",
      "Condition": { 
        "StringEquals": {
          "AWS:SourceAccount": "sourceAccountID"
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
      "Resource": "arn:aws:s3:::amzn-s3-demo-bucket/[optional] prefix/AWSLogs/sourceAccountID/Config/*",
      "Condition": { 
        "StringEquals": { 
          "s3:x-amz-acl": "bucket-owner-full-control",
          "AWS:SourceAccount": "sourceAccountID"
        }
      }
    }
  ]
}
```

### Check
Check your AWS Config is enabled manually.

For example, you can check them in the config aggregator.