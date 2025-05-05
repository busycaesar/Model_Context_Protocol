import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import admin from "firebase-admin";

class Firebase {
  private db: FirebaseFirestore.Firestore;

  constructor(serviceAccountKeyFile: string) {
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccountKeyFile),
    });

    this.db = admin.firestore();
  }

  fetchCollection = async () => {
    try {
      const collections = await this.db.listCollections();
      return collections.map((collection) => collection.id);
    } catch (error) {
      throw error;
    }
  };

  addNewDocument = async (collectionName: string, document: any) => {
    try {
      const _document = await this.db.collection(collectionName).doc();

      _document.set(document);
    } catch (error) {
      throw error;
    }
  };

  getDocuments = async (collectionName: string) => {
    const documents = await this.db.collection(collectionName).get();

    const _documents: any[] = [];

    documents.forEach((document) => {
      _documents.push(document.data());
    });

    return _documents;
  };
}

const serviceAccountKeyFile = process.env.SERVICE_ACCOUNT_KEY_FILE;

if (!serviceAccountKeyFile)
  throw new Error("SERVICE_ACCOUNT_KEY_FILE path not provided.");

const firebase = new Firebase(serviceAccountKeyFile);

// Create server instance
const server = new McpServer({
  name: "firebase",
  version: "1.0.0",
  capabilities: {
    resources: {},
    tools: {},
  },
});

server.tool(
  "fetch-collections",
  "Get all the collections stored in the firebase",
  async (_extra) => {
    const collections = await firebase.fetchCollection();
    return {
      content: [{ type: "text", text: JSON.stringify(collections) }],
    };
  }
);

server.tool(
  "add-new-document",
  "Add new document into the existing or new collection. If the collection does not exists, the function creates it automatically.",
  { collectionName: z.string(), document: z.any() },
  async ({ collectionName, document }) => {
    await firebase.addNewDocument(collectionName, document);
    return {
      content: [
        {
          type: "text",
          text: `The new document is added to the collection ${collectionName}`,
        },
      ],
    };
  }
);

server.tool(
  "get-documents",
  "Get all the documents from the existing collections in the firebase",
  { collectionName: z.string() },
  async ({ collectionName }) => {
    const documents = await firebase.getDocuments(collectionName);
    return {
      content: [{ type: "text", text: JSON.stringify(documents) }],
    };
  }
);

const main = async () => {
  const transport = new StdioServerTransport();

  await server.connect(transport);
};

main().catch((error) => {
  console.log("Error while running the main function.", error);
  process.exit(1);
});
