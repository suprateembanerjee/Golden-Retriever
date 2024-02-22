# Author: Suprateem Banerjee [www.github.com/suprateembanerjee]

from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import BaseRetriever, Document
import pinecone
import sentence_transformers
from typing import Any, List

class PineconeRetriever(BaseRetriever):
    db: pinecone.data.index.Index = None
    embedding: sentence_transformers.SentenceTransformer = None
    collection: Any

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun, **kwargs: Any) -> List[Document]:
        
        query = self.embedding.encode(query, show_progress_bar=False).tolist()
        out = []
        results = self.db.query(vector=query, top_k=20)['matches']
        
        for match in results:
            out.append(Document(page_content=self.collection.find({'_id':int(match['id'])})[0]['Message'], metadata= {'index': match['id'] }))

        return out