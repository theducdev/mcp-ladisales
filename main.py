"""
Main entry point for LaDiSales MCP server.
This file is responsible for starting and running the MCP server with streamable-http support.
"""

from server import mcp

def main():
    print("🔧 MCP Server is starting with streamable-http support...")
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()