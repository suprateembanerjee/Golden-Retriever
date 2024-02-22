# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64 
import pickle
from bs4 import BeautifulSoup 
from datetime import date, timedelta, datetime
import os
import re
import pymongo
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def getEmails(mongodb_url:str): 
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None
  
    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists("res/token.json"):
        creds = Credentials.from_authorized_user_file("res/token.json", SCOPES)
  
    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file('res/credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0) 
  
        # Save the access token in token.pickle file for the next run 
        # with open('res/token.pickle', 'wb') as token: 
        #     pickle.dump(creds, token) 
  
    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 

    today = date.today()
    t_minus_2m = today - timedelta(60)

    # Dates have to formatted in YYYY/MM/DD format for gmail
    query = f"before: {today.strftime('%Y/%m/%d')} after: {t_minus_2m.strftime('%Y/%m/%d')} in:inbox category:primary"

  
    # request a list of all the messages
    result = service.users().messages().list(userId='me', q=query).execute()
  
    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages')
  
    # messages is a list of dictionaries where each dictionary contains a message id. 

    mongo_client = pymongo.MongoClient(mongodb_url)
    db = mongo_client['emails_db']

    try:
        emails_collection = db['emails']
        emails_collection.drop()
    except pymongo.errors.OperationFailure:
        pass
        
    emails_collection = db['emails']

    i = 1

    # iterate through all the messages 
    for msg in messages: 
        # Get the message from its id 
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 

        # Get the timestamp when mail was received
        timestamp = datetime.fromtimestamp(float(txt['internalDate']) / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
  
        # Use try-except to avoid any Errors 
        try: 
            # Get value of 'payload' from dictionary 'txt' 
            payload = txt['payload'] 
            headers = payload['headers'] 

            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it. 
            # Get the data and decode it with base 64 decoder. 
            if 'parts' not in payload:
                data = payload['body']['data']
            else:
                parts = payload.get('parts')[0]
                data = parts['body']['data'] 
            data = data.replace("-","+").replace("_","/") 
            decoded_data = base64.b64decode(data) 

            soup = BeautifulSoup(decoded_data, features="html.parser")

            for script in soup(["script", "style"]):
                script.extract() 

            body = soup.get_text(strip=True)
            body = re.sub(r"https?:[^\s]+", '', body)
            body = os.linesep.join([s for s in iter(body.splitlines()) if s.strip() and re.search('[a-zA-Z]', s)])

            email = {
                '_id' : i,
                'Subject' : subject,
                'Sender': sender,
                'Message': body
            }

            emails_collection.insert_one(email)
            
            i += 1

        except Exception as e: 
            print("Exception!!", e)


if __name__ == "__main__":
  getEmails()