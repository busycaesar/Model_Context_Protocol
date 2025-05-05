The following documentation has been prepared with reference to the [MCP Website](https://modelcontextprotocol.io/quickstart/client). These instructions are intended for setting up the MCP client on Linux/MacOS. If you are using a Windows machine, please refer to the official website for the appropriate commands.

# Steps to create the MCP client using Python:

## System Requirements

- Latest Python version
- Latest `uv` version

## Setup the environment

- Create the setup for the project.

```bash
# Create the directory for the MCP client.
uv init [desired client name]
cd [desired client name]

# Create the virtual environment and activate it.
python -m venv .venv
source .venv/bin/activate

# Install dependencies
uv add mcp anthropic python-dotenv

touch [desired server file name]
```

- Setup the API Key

```bash
# .venv
ANTHROPIC_API_KEY=<your key here>
```

- Paste the server code into the new file and explain it.
