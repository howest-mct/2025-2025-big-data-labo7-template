import os
import random
import time
import logging

from dotenv import load_dotenv
import boto3
import botocore.exceptions

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DELIVERY_STREAM_NAME = os.getenv("DELIVERY_STREAM_NAME")
REGION_NAME = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

logger.info("Using delivery stream: %s", DELIVERY_STREAM_NAME)
logger.info("Using AWS region: %s", REGION_NAME)

if not all([DELIVERY_STREAM_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
    logger.error("Missing AWS credentials or stream name, please configure .env")
    raise SystemExit(1)

client = boto3.client(
    "firehose",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

file_path = "/data/exportVideos.json"
if not os.path.exists(file_path):
    logger.error("exportVideos.json not present at %s", file_path)
    raise SystemExit(1)

with open(file_path) as file:
    _ = file.readline()

    for line in file:
        data = line.strip()
        if not data:
            continue

        logger.info("Sending data: %s", data[:100])

        try:
            client.put_record(
                DeliveryStreamName=DELIVERY_STREAM_NAME,
                Record={"Data": data.encode("utf-8")},
            )
        except botocore.exceptions.ClientError as e:
            logger.exception("PutRecord failed")
            break

        sleep = random.randint(50, 100) / 50.0
        time.sleep(sleep)
