# Firebase MCP Server using Node.js with VS Code copilot integration

The following documentation has been prepared with reference to the [MCP Website](https://modelcontextprotocol.io/quickstart/server#node).

## System Requirements

- `>= 16 node`
- `npm`

## Create Firebase MCP Server

- Create a new node project and install required dependencies

```bash
npm init -y
npm install @modelcontextprotocol/sdk zod firebase-admin
npm install -D @types/node typescript
```

- Create the required file

```bash
mkdir src
touch src/index.ts
```

- Update `package.json` to all the following.

```json
"type": "module"
"scripts.build": "tsc && chmod 755 build/index.js"
```

- Create `tsconfig.json` and add the following

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

- Add the code in `src/index.ts` file.

```ts
// Import required functions from the MCP sdk.
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Import the admin from firebase-admin to manage the database.
import admin from "firebase-admin";

// Import zod for desclaring the schema type and validating the data.
import { z } from "zod";

// Firebase class to encapsulate all the functions related to firebase.
class Firebase {
  // Instance of the firebase DB.
  private db: FirebaseFirestore.Firestore;

  // Receives the absolute path where the json file with credentails for the firebase account is stored.
  constructor(serviceAccountKeyFile: string) {
    // Initialize the firebase application using the credentials.
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccountKeyFile),
    });

    // Pass the instance of the firesotre to the class variable.
    this.db = admin.firestore();
  }

  // Function to fetch all the collections from the firebase.
  fetchCollection = async () => {
    try {
      const collections = await this.db.listCollections();

      return collections.map((collection) => collection.id);
    } catch (error) {
      throw error;
    }
  };

  // Function to add a new document in a new or existing collection.
  addNewDocument = async (collectionName: string, document: any) => {
    try {
      const _document = await this.db.collection(collectionName).doc();

      return _document.set(document);
    } catch (error) {
      throw error;
    }
  };

  // Get all the documents from a specific collection.
  getDocuments = async (collectionName: string) => {
    const documents = await this.db.collection(collectionName).get();

    const _documents: any[] = [];

    documents.forEach((document) => {
      _documents.push(document.data());
    });

    return _documents;
  };
}

// Initialize a new instance of the class that we created by passing the absolute path where the credentails for the firebase is stored.
const firebase = new Firebase(
  "/home/busycaesar/projects/personal/mcp/firebase-node/firebase-admin-cred.json"
);

// Create a new MCP server instance
const server = new McpServer({
  name: "firebase",
  version: "1.0.0",
  // Includes the resources and tools provided by the MCP server.
  capabilities: {
    // Data elements that the MCP server exposes to the clients like File content, DB record etc.
    resources: {},
    // Executable functions that the MCP server exposes, allowing the clients and LLMs to perform action.
    tools: {},
  },
});

// Creating a new tool for the MCP server.
server.tool(
  // Name of the tool.
  "add-new-document",
  // Description of the tool.
  "Add new document into the existing or new collection. If the collection does not exists, the function creates it automatically.",
  // Required arguments for executing the function.
  // These arguments are figured out by the LLM from the user's prompt.
  // If the required data is not present, the LLM prompts the user to enter the data.
  { collectionName: z.string(), document: z.any() },
  // Logic that the tool performs when called.
  async ({ collectionName, document }) => {
    // Call the fucntion, add new document from the firebase class, along with passing the collection name and document.
    await firebase.addNewDocument(collectionName, document);
    // Return the content with its type and data.
    // Standardize response format.
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

// Main function to start the server.
const main = async () => {
  // Initiating the transportation method for the connection between the MCP server and the client.
  // In this case, we will be usign stdio since both our MCP server and the client will be running on the same local machine.
  const transport = new StdioServerTransport();

  // Calling the connect method of the server class by passing the prefered transportation method.
  await server.connect(transport);
};

// Executing the main method along with error handling.
main().catch((error) => {
  console.log("Error while running the main function.", error);
  process.exit(1);
});
```

- Get the Private Key from the [Firebase console](https://console.firebase.google.com/u/0/project/mcp-server-8facf/settings/serviceaccounts/adminsdk).

- Store the json file at any specific location.

- Update the absolute location of the json file in the code when declaring the firebase instance.

```ts
const firebase = new Firebase(
  "absolute/location/of/json/file"
);
```

- Run `npm run build` to create the build version.

## Add and start the MCP server through VS Code.

- Use the following command in command palette.

```bash
>MCP: Add Server
```

- Select 'Command (stdio)'.

- Write `node` for the command.

- Add the name for the server.

- Choose 'Workspace Settings' to add the MCP server only to the current workspace.

- Add the following in the `.vscode/mcp.json`

```json
{
  "servers": {
    "node-firebase": {
      "type": "stdio",
      "command": "node",
      "args": [
        "path to MCP server file"
      ]
    }
  }
}
```

- Start the MCP Server by using the following command in command palette.

```bash
>MCP: List Servers
```

- Choose the name of the MCP server that we created.

- Click 'Start Server' to start the server.

## Use the MCP server through VS Code Copilot

- Once the MCP server is started, toggle the copilot chat.

- Click `Add Context` to add the required tool/s.

- Use Chatbot to use the added tool/s.
