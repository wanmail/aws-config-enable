import boto3

import sso
import recorder
import s3

SSO_LOGIN_URL = 'https://example.awsapps.com/start/#'
ROLE_NAME = 'SecurityAudit'

BUCKET_NAME = 'config-bucket-example'

REGION_LIST = ["us-east-1"]


def setup_recorder(client, account_id):
    client.put_configuration_recorder(
        ConfigurationRecorder=recorder.get_recoder_config(account_id)
    )


def setup_delivery(client):
    client.put_delivery_channel(
        DeliveryChannel=recorder.get_delivery_config(BUCKET_NAME)
    )


def start_recoder(client):
    client.start_configuration_recorder(
        ConfigurationRecorderName=recorder.RECORDER_NAME
    )


def setup_s3_policy(accounts):
    import json
    print(json.dumps(s3.get_s3_policy(BUCKET_NAME, accounts), indent=4))


if __name__ == "__main__":
    # use sso token
    # `aws sso login` to get the credentials first
    token = sso.get_sso_access_token(SSO_LOGIN_URL)

    accounts = []
    for credential in sso.get_credentials(ROLE_NAME, token):
        for region in REGION_LIST:
            accounts.append(credential.account_id)
            client = boto3.client('config', region_name=region, aws_access_key_id=credential.access_key,
                                  aws_secret_access_key=credential.secret_key, aws_session_token=credential.session_token)

            setup_recorder(client, credential.account_id)
            setup_delivery(client)
            start_recoder(client)

            setup_s3_policy(accounts)

            print(f"Config service setup for {
                  credential.account_id} in {region}")
