import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from ollama import Client

from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = Client()
        self.tools = []
        
    def _check_script_ext(self, script_path):
        is_python = script_path.endswith(".py")
        is_js = script_path.endswith(".js")

        if is_python: return "python"
        elif is_js: return "node"

        return None

    async def connect_to_server(self, server_script):
        """
        Connect to the MCP Server.

        Args:
            server_script: Path to the server script.
        """

        command = self._check_script_ext(server_script)

        if not command:
            raise ValueError("Server script must be JS or Python.")
        
        server_params = StdioServerParameters(
            command=command,
            args=[server_script],
            env=None
        )

        self.stdio, self.write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        response = await self.session.list_tools()

        self.tools = [{
            "name": tool.name,
            "description": tool.description,
            "parammeters": tool.inputSchema
        } for tool in response.tools]

        print("\nConnected to server with tools:", self.tools)

    async def process_query(self, query):
        """
        Process the query using the LLM.

        Args:
            query: The query to process.
        """
        
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = self.client.chat(
            model="qwen2.5:3b",
            messages=messages,
            tools=self.tools
        )

        print(response.message)

        final_text = []
        assistant_message_content = []

        content = response.message.content
        tool_calls = response.message.tool_calls

        if content:
            final_text.append(content)
            assistant_message_content.append(content)
        elif tool_calls:
            for tool in tool_calls:
                tool_name = tool.function.name
                tool_args = tool.function.arguments

                result = await self.session.call_tool(
                    tool_name,
                    dict(tool_args)
                )

                final_text.append(f"[Calling tool ${tool_name} with args {tool_args}]")

                assistant_message_content.append(tool)

                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })

                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "content": result.content[0].text
                    }]
                })

                response = self.client.chat(
                    model="qwen2.5:3b",
                    messages=messages
                )

                final_text.append(result.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """
        Interactive chat loop.
        """
        print("\nMCP Client Started:")
        print("\nType the query or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)

                print("\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())