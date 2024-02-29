# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]
# Usage: python rag.py "What events am I attending this week?""

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.chains import ConversationalRetrievalChain
from typing import Any, List
import pinecone
import sentence_transformers
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import BaseRetriever, Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
import json
import argparse

from custom_retrievers import PineconeRetriever
from utils import setup_pinecone, setup_mongo


def perform_rag(prompt:str, 
				pinecone_api_key:str, 
				cohere_api_key:str, 
				pinecone_index:str, 
				mongodb_url:str, 
				embedding_model:str='WhereIsAI/UAE-Large-V1') -> None:


	embedding = sentence_transformers.SentenceTransformer(embedding_model)

	emails, emails_collection, event_emails_collection = setup_mongo(mongodb_url)

	data = {}
	for email in emails:
		data[str(email['_id'])] = embedding.encode(email['Message'], show_progress_bar=False)

	pinecone_idx = setup_pinecone(pinecone_api_key, pinecone_index, data)

	results = [emails_collection.find({'_id':int(match['id'])})[0] for match in pinecone_idx.query(vector=embedding.encode(prompt, show_progress_bar=False).tolist(), top_k=20)['matches']]

	retriever = PineconeRetriever(db=pinecone_idx, embedding=embedding, collection=emails_collection)
	docs = retriever.get_relevant_documents(prompt)

	compressor = CohereRerank(cohere_api_key=cohere_api_key, top_n = 10)
	compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
	compressed_docs = compression_retriever.get_relevant_documents(prompt)

	for doc in compressed_docs:
		event_emails_collection.insert_one(emails_collection.find({'_id':int(doc.metadata['index'])})[0])
	
	return list(event_emails_collection.find())

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Query Processor')
	parser.add_argument('query', type=str, help='Query to process')
	args = parser.parse_args()
	perform_rag(args.query)
	print('Sucess!')

