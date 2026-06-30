from pinecone import Pinecone
from dotenv import load_dotenv
import os
import random

load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["PINECONE_INDEX_HOST"])
messages = [
    "🍤Looking for the perfect comback...",
    "📦Opening the vault...",
    "📪Asking Newman...",
]


def search(query):
    try:
        message = random.choice(messages)
        message_status = {"SEID": "/", "Character": "/", "Dialogue": message}
        yield message_status

        results = index.search(
            namespace="__default__",
            query={"inputs": {"text": query}, "top_k": 5},
            fields=["SEID", "Character", "Dialogue"],
        )
        refrences = [result["fields"] for result in results["result"]["hits"]]
        yield refrences
    except Exception as e:
        print(e)
        return [
            {
                "SEID": "/",
                "Character": "/",
                "Dialogue": "🎶 Believe it or not, the service has a problem,\nplease leave message at the beep.\nThe usage maxed out, or you'd get a response, we are so sorry!\nBelieve it or not, a problem",
            },
            {
                "SEID": "/",
                "Character": "Pinecone",
                "Dialogue": e,
            },
        ]
