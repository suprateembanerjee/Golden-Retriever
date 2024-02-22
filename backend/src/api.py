# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import json

from rag import perform_rag
from get_emails import getEmails

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])
# CORS(app, origins=['http://rag-frontend:5173'])
api = Api(app)

class Rag(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('query', type=str, required=True, location='json', help='Input sentence')
		self.reqparse.add_argument('pinecone_api_key', type=str, required=True, location='json', help='Pinecone API Key')
		self.reqparse.add_argument('cohere_api_key', type=str, required=True, location='json', help='Cohere API Key')
		self.reqparse.add_argument('pinecone_index', type=str, required=True, location='json', help='Pinecone Index')
		self.reqparse.add_argument('mongodb_url', type=str, required=True, location='json', help='Mongodb URL')
		super().__init__()

	def post(self):

		args = self.reqparse.parse_args()

		query = args['query']

		pinecone_api_key = args['pinecone_api_key']
		cohere_api_key = args['cohere_api_key']
		pinecone_index = args['pinecone_index']
		mongodb_url = args['mongodb_url']


		events_email_collection = perform_rag(query, pinecone_api_key, cohere_api_key, pinecone_index, mongodb_url)

		return {"emails": events_email_collection}, 200

class GetEmails(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('mongodb_url', type=str, required=True, location='json', help='Mongodb URL')
		super().__init__()

	def post(self):
		args = self.reqparse.parse_args()

		getEmails(args['mongodb_url'])

		return {"status": "Success"}, 200

api.add_resource(Rag, '/rag')
api.add_resource(GetEmails, '/get_emails')

if __name__=='__main__':

	app.run(debug=True, host='0.0.0.0')