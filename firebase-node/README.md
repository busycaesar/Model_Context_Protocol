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

      return _document.set(document);
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
```

- Run `npm run build` to create the build version.

- Get the Private Key from the [Firebase console](https://console.firebase.google.com/u/0/project/mcp-server-8facf/settings/serviceaccounts/adminsdk).

- Store the json file at any specific location.

- Create `.env` file and add the following.

```.env
SERVICE_ACCOUNT_KEY_FILE='Absolute location to the downloaded json file from Firebase'
```

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
      ],
      "envFile": "path to the env file."
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
