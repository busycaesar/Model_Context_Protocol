import firebase_admin
from firebase_admin import credentials, firestore
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("firebase")

class Firebase:
    def __init__(self, service_account_key_file):
        cred = credentials.Certificate(service_account_key_file)
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    async def fetch_collections(self):
        return [collection.id for collection in self.db.collections()]

    async def add_new_document(self, collection_name, document):
        _document = self.db.collection(collection_name).document()
        return _document.set(document)
    
    async def get_documents(self, collection_name):
        collection = self.db.collection(collection_name)
        documents = collection.get()

        return [doc.to_dict() for doc in documents]
    
firebase = Firebase("./.env.firebase.json")

@mcp.tool()
async def fetch_collections():
    """
    Fetches all the collections from the firebase.
    """

    return firebase.fetch_collections()

@mcp.tool()
async def add_new_document(collection_name, document):
    """
    Adds a new document into the collection.

    Args:
        collection_name: The name of the existing or new collection.
        document: The document to add into the collection.
    """

    firebase.add_new_document(collection_name, document)

@mcp.tool()
async def get_documents(new_collection_name):
    """
    Get all the document from the collection.

    Args:
        collection_name: Name for the new collection.
    """

    firebase.get_documents(new_collection_name)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')