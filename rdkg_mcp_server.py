# rdkg_mcp_server.py
import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

RDKG_API = "http://localhost:8000"
server = Server("rdkg-mcp")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_disease",
            description="Search for a rare disease by name or synonym in RDKG. Returns MONDO ID, Orphanet ID, and disease names.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Disease name or partial name"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_disease",
            description="Get full details and cross-references for a disease by MONDO ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mondo_id": {"type": "string", "description": "MONDO ID e.g. MONDO:0007765"}
                },
                "required": ["mondo_id"]
            }
        ),
        Tool(
            name="get_phenotypes",
            description="Get HPO phenotypes associated with a rare disease. Includes frequency and onset data from HPOA.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mondo_id": {"type": "string"}
                },
                "required": ["mondo_id"]
            }
        ),
        Tool(
            name="get_variants",
            description="Get ClinVar pathogenic variants for a rare disease.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mondo_id": {"type": "string"}
                },
                "required": ["mondo_id"]
            }
        ),
        Tool(
            name="get_treatments",
            description="Get MAxO medical treatment actions for a rare disease.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mondo_id": {"type": "string"}
                },
                "required": ["mondo_id"]
            }
        ),
        Tool(
            name="diseases_by_phenotype",
            description="Find rare diseases associated with a given HPO phenotype term. Useful for differential diagnosis support.",
            inputSchema={
                "type": "object",
                "properties": {
                    "hpo_id": {"type": "string", "description": "HPO ID e.g. HP:0000278"}
                },
                "required": ["hpo_id"]
            }
        ),
        Tool(
            name="run_sparql",
            description="Run a custom SPARQL query against the RDKG RDF endpoint for advanced federated queries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SPARQL SELECT query"}
                },
                "required": ["query"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    async with httpx.AsyncClient() as client:
        try:
            if name == "search_disease":
                r = await client.get(f"{RDKG_API}/disease/search",
                                     params={"name": arguments["name"]})
            elif name == "get_disease":
                r = await client.get(f"{RDKG_API}/disease/{arguments['mondo_id']}")
            elif name == "get_phenotypes":
                r = await client.get(f"{RDKG_API}/disease/{arguments['mondo_id']}/phenotypes")
            elif name == "get_variants":
                r = await client.get(f"{RDKG_API}/disease/{arguments['mondo_id']}/variants")
            elif name == "get_treatments":
                r = await client.get(f"{RDKG_API}/disease/{arguments['mondo_id']}/treatments")
            elif name == "diseases_by_phenotype":
                r = await client.get(f"{RDKG_API}/phenotype/{arguments['hpo_id']}/diseases")
            elif name == "run_sparql":
                r = await client.post(f"{RDKG_API}/sparql",
                                      params={"query": arguments["query"]})
            else:
                return CallToolResult(content=[TextContent(type="text", text="Unknown tool")])

            r.raise_for_status()
            return CallToolResult(content=[TextContent(type="text", text=r.text)])

        except Exception as e:
            return CallToolResult(content=[TextContent(type="text", text=f"Error: {e}")])


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
