import boto3

def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-east-1")
    response = ses_client.verify_email_identity(
        EmailAddress= email
    )
    print(response)


def send_plain_email():
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "amol@nirenshah.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, world!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="FibonacciiRetracement@gmail.com",
    )

send_plain_email()


