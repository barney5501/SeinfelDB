# 🥨 SeinfelDB - Find the perfect comeback 🍤

A smart vector based search for seinfeld references.
[SeinfelDB](https://huggingface.co/spaces/Barney5501/seinfelDB)

Gradio interface used to search for the perfect seinfeld reference for any situation,\
Using Pinecone vector db for semantic matching.

## Stack 🛠

- **🔢 Data Ingestion:** Custom Python batch-upload script.
- **📦 Environment & Package Management:** Astral's uv.
- **🔀 Vector Database:** Pinecone (Serverless) utilizing Integrated Embeddings.
- **💻 Web Interface:** Gradio app.
- **🤗 Hosting & Deployment:** Hugging Face Spaces.

## Overview 💡

All the dialogue lines from the show are upserted to Pinecone, using their SDK [see: `pinecone_upsert.py`].\
*note: the raw source of the script scraping is currently borrowed from [4m4n5's linked repo](https://github.com/4m4n5/the-seinfeld-chronicles).*

After the Pinecone index is populated with embeddings (I used the integrated embeddings option in the index), use the `API key` and the `Index Host` to send queries through the SDK.

### Deployment 🚀

This is all wrapped in a simple Gradio app, and synced through GitHub Actions to HuggingFace, available in [this link](https://huggingface.co/spaces/Barney5501/seinfelDB).

HuggingFace expects a YAML frontmatter in the README.md file, I implemented a workaround, by putting the frontmatter in a .hfconfig file, and adding a simple `mv` command to the Actions workflow YAML, overwriting the README.md with the .hfconfig before the sync to HuggingFace.

## Local Setup 🏠

First, make sure you have the data and a pinecone index. \
Then:

1. Clone this repo.
2. run `uv sync`.
3. create a .env file with
    - PINECONE_API_KEY
    - PINECONE_INDEX_HOST
4. run the upsert script: `uv run pinecone_upsert.py`
5. run the app: `uv run app.py`

Alternatively, you can just replace the SDK calls with a function that yields a constant/random responses for quick local development. see `vectorsearch.py/search()`.

<!-- 
ROADMAP:
REDIS
TELEGRAM
ENRICH CONTEXT -->