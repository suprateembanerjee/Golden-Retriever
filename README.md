# Golden-Retriever
A Langchain-based RAG application using Angle Embeddings and Cohere Reranker to fetch relevant emails based on query.

<img width="1134" alt="Screenshot 2024-02-21 at 11 41 52 PM" src="https://github.com/suprateembanerjee/Golden-Retriever/assets/26841866/25b84338-cdf0-4d7c-afcf-bc3dd60da425">

## Usage

### Docker Compose
`docker compose up`

The app is served on `localhost:5173/`

![rag](https://github.com/suprateembanerjee/Golden-Retriever/assets/26841866/c25261c2-5b23-4c46-a031-2752c091afa4)

## Pipeline

### Gmail API

The [Gmail API](https://developers.google.com/gmail/api/guides) is used to download emails into a specified mongo database.

Once set up, the credential files are to be placed in a folder titled *res* in [backend](backend/)

#### Customization

The default behavior is to collect all emails in the *Primary* folder in the last 60 days. This can be customized by modifying the [get_emails script](backend/src/get_emails.py) lines 49-52.

### Retriever

The custom Retriever is composed of a [AnglE](https://github.com/SeanLee97/AnglE) embedding model and a [Pinecone](https://app.pinecone.io) Vector Database. Pinecone offers a free API Index, which was used to build this project.

### Re-Ranker

The [Cohere Re-ranker](https://cohere.com/rerank) was used to re-rank 20 retrievals into 10 most relevant documents, which were stored in the Mongo database, and displayed in the web application.

## Containers

### Front-End

The container serves a React App built using [ViteJS](https://vitejs.dev) containing custom CSS elements for aesthetic purposes. The app makes `fetch` requests based on context and serves the result in a read-only Textbox. The API is served on `LocalHost:5173/`.

### Back-End

The Flask API serves two distinct endpoints: 
  1. `/get_emails`
     Used to invoke the Gmail API to collect emails from inbox.
  2. `/rag`
     Used to perform the Retrieval Pipeline.

#### Considerations

The docker containers need increased memory to perform the retrieval tasks, failing which the backend container may crash.

### Mongo

The mongo v7.0 database interacts solely with the backend container, for storing all emails in a collection titled **emails** and retrieved emails in a collection titled **event-emails**.

## Conclusions

Golden Retriever was a personal project I undertook after missing an event at Northeastern on a Wednesday in February, 2024. The project involves designing and developing a RAG pipeline based on personal research, containerized into three containers bridged by an underlying docker network and orchestrated using docker-compose. The query-based email retrieval step takes a bit of time at the moment. There are some security considerations such as passing of API Keys via REST API Calls, which are subject to attacks, but in this context, which is completely local, has been deemed to be sufficient. A LLM can be retrofitted using an additional line of python code, using Langchain `ConversationalRetrievalChain` but has not been implemented as a part of the project due to compute restrictions of running it locally. LLMs such as Llama 2 7B has been tested and works as expected.
