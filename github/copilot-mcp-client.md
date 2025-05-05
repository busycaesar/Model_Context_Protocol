# Steps to create the MCP client using Copilot in VS Code:

## System Requirements

- VS Code Insiders

## Setup the environment

- Open settings and search for MCP.
- Click `Edit in settings.json`
- List the server with the information as required.

### Sample

```json
"server name": {
  "command": "uv", 
  "args": [
    "--directory",
    "Absolute path to the directory",
    "run",
    "Name of the server file in the directory"
  ],
  // Environment variable, if any.
  "env": {
    "Key": "Value"
  }
}
```

- Open the Copilot chat and click on the tools icon and it will load the tools.
- Once the tools are successfully loaded, use the chat to demonstration the project.
