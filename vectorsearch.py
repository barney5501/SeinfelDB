from pinecone import Pinecone
from dotenv import load_dotenv
import os
import random
from pydantic import BaseModel, Field
from typing import List, Generator

load_dotenv()


class Reference(BaseModel):
    seid: str = Field(alias="SEID")
    character: str = Field(alias="Character")
    dialogue: str = Field(alias="Dialogue")


pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["PINECONE_INDEX_HOST"])
messages = [
    "🍤Looking for the perfect comback...",
    "📦Opening the vault...",
    "📪Asking Newman...",
]


def search(query: str) -> Generator[List[Reference]]:
    try:
        message = random.choice(messages)
        message_status = Reference(SEID="/", Character="/", Dialogue=message)
        yield [message_status]

        results = index.search(
            namespace="__default__",
            query={"inputs": {"text": query}, "top_k": 5},
            fields=["SEID", "Character", "Dialogue"],
        )
        refrences = [
            Reference.model_validate(result["fields"])
            for result in results["result"]["hits"]
        ]
        yield refrences
    except Exception as e:
        print(e)
        yield [
            Reference(
                SEID="/",
                Character="/",
                Dialogue="🎶 Believe it or not, the service has a problem,\nplease leave message at the beep.\nThe usage maxed out, or you'd get a response, we are so sorry!\nBelieve it or not, a problem",
            ),
            Reference(
                SEID="/",
                Character="Pinecone",
                Dialogue=str(e),
            )
        ]
