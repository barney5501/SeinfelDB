from pinecone import Pinecone
from dotenv import load_dotenv
import os
import random
from pydantic import BaseModel, Field
from typing import List, Generator
from messages import messages

load_dotenv()


class Reference(BaseModel):
    seid: str = Field(alias="SEID")
    character: str = Field(alias="Character")
    dialogue: str = Field(alias="Dialogue")


pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["PINECONE_INDEX_HOST"])


def search(query: str) -> Generator[List[Reference], None, None]:
    try:
        message = random.choice(messages["loading"])
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
                Dialogue=messages["db_error"],
            ),
            Reference(
                SEID="/",
                Character="Pinecone",
                Dialogue=str(e),
            ),
        ]
