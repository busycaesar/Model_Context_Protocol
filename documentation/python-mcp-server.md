Following documentation is taken with the reference of [MCP Website](https://modelcontextprotocol.io/quickstart/server#core-mcp-concepts). The following commands are suitable for Linux/MacOS. Check out the website for the command for Windows Machine.

# Steps to create the MCP server using Python:

## System Requirements

- `>= Python 3.10`
- `>= Python MCP SDK 1.2.0`

## Setup the environment

- Install `uv` using the following script.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Restart the terminal to ensure that the `uv` commands gets picked up.

- Create the setup for the project.

```bash
# Create the directory for the MCP server.
uv init [desired server name]
cd [desired server name]

# Create the virtual environment and activate it.
python -m venv .venv
source .venv/bin/activate

# Install dependencies
uuv add "mcp[cli]" httpx

touch [desired server file name]
```

- Paste the server code into the new file.
