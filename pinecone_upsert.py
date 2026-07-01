import os
from dotenv import load_dotenv
from pinecone import Pinecone
import json

load_dotenv()
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_HOST = os.environ["PINECONE_INDEX_HOST"]

with open("seinfeld.json", "r") as seinfile:
    records = json.load(seinfile)


pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(host=INDEX_HOST)

BATCH_SIZE = 64
for i in range(13504, len(records), BATCH_SIZE):
    batch = records[i : i + BATCH_SIZE]
    print(f"{i}/{len(records)}")
    print("...")
    index.upsert_records(namespace="__default__", records=batch)
print("done")
