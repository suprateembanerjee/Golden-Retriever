# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]

import pinecone
from langchain.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader
import json
import pymongo

def setup_mongo(mongo_url:str) -> dict:

	mongo_client = pymongo.MongoClient(mongo_url)
	db = mongo_client['emails_db']
	emails_collection = db['emails']

	try:
		event_emails_collection = db['event_emails']
		event_emails_collection.drop()
	except pymongo.errors.OperationFailure:
		pass
		
	event_emails_collection = db['event_emails']

	emails = list(emails_collection.find({}))

	return emails, emails_collection, event_emails_collection

def setup_pinecone(api_key:str, index_name:str, data:dict):
	pc = pinecone.Pinecone(api_key=api_key)

	if index_name in pc.list_indexes():
		pc.delete_index(index_name)
		pc.create_index(name=index_name, 
						dimension=1024, 
	    				metric="cosine", 
	    				spec=pinecone.PodSpec(environment="us-west1-gcp", 
	    									  pod_type="p1.x1"))
	pinecone_idx = pc.Index(index_name)

	for i in data:
		pinecone_idx.upsert([(i, data[i])])

	return pinecone_idx
