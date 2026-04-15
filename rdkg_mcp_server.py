import asyncio, os, httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

RDKG_API = os.environ.get("RDKG_API", "http://localhost:8000")
server = Server("rdkg-mcp")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="search_disease", description="Search for a rare disease by name in RDKG. Returns disease IDs and names.", inputSchema={"type":"object","properties":{"name":{"type":"string","description":"Disease name or partial name"}},"required":["name"]}),
        Tool(name="get_disease", description="Get full details for a disease by its RDKG ID.", inputSchema={"type":"object","properties":{"disease_id":{"type":"string","description":"Disease ID e.g. MONDO:0007947"}},"required":["disease_id"]}),
        Tool(name="get_phenotypes", description="Get HPO phenotypes for a disease. Returns HPO IDs and names from HPOA.", inputSchema={"type":"object","properties":{"disease_id":{"type":"string"}},"required":["disease_id"]}),
        Tool(name="get_related", description="Get all entities related to a disease: genes, drugs, variants via graph traversal.", inputSchema={"type":"object","properties":{"disease_id":{"type":"string"}},"required":["disease_id"]}),
        Tool(name="diseases_by_phenotype", description="Find rare diseases associated with an HPO phenotype term. Core use case for phenotype-driven differential diagnosis.", inputSchema={"type":"object","properties":{"hpo_id":{"type":"string","description":"HPO ID e.g. HP:0000278"}},"required":["hpo_id"]}),
        Tool(name="search_phenotype", description="Search HPO phenotype terms by name to find their IDs.", inputSchema={"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}),
        Tool(name="search_drug", description="Search for a drug by name in RDKG.", inputSchema={"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}),
        Tool(name="get_stats", description="Get RDKG statistics: node and edge counts by type. Shows full graph scope.", inputSchema={"type":"object","properties":{}}),
        Tool(name="run_cypher", description="Run a read-only Cypher query against RDKG Neo4j for custom graph traversals.", inputSchema={"type":"object","properties":{"query":{"type":"string","description":"Cypher query"}},"required":["query"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if name == "search_disease":
                r = await client.get(f"{RDKG_API}/disease/search", params={"name": arguments["name"]})
            elif name == "get_disease":
                r = await client.get(f"{RDKG_API}/disease/{arguments['disease_id']}")
            elif name == "get_phenotypes":
                r = await client.get(f"{RDKG_API}/disease/{arguments['disease_id']}/phenotypes")
            elif name == "get_related":
                r = await client.get(f"{RDKG_API}/disease/{arguments['disease_id']}/related")
            elif name == "diseases_by_phenotype":
                r = await client.get(f"{RDKG_API}/phenotype/{arguments['hpo_id']}/diseases")
            elif name == "search_phenotype":
                r = await client.get(f"{RDKG_API}/phenotype/search", params={"name": arguments["name"]})
            elif name == "search_drug":
                r = await client.get(f"{RDKG_API}/drug/search", params={"name": arguments["name"]})
            elif name == "get_stats":
                r = await client.get(f"{RDKG_API}/stats")
            elif name == "run_cypher":
                r = await client.post(f"{RDKG_API}/cypher", params={"query": arguments["query"]})
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

            if r.status_code == 404:
                return [TextContent(type="text", text="Not found in RDKG.")]
            r.raise_for_status()
            return [TextContent(type="text", text=r.text)]

        except httpx.ConnectError:
            return [TextContent(type="text", text=f"Cannot reach RDKG API at {RDKG_API}. Run: docker compose up -d")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
