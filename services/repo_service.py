from codebase_rag.main import _initialize_services_and_agent, _setup_common_initialization, init_session_log, log_session_event, get_session_context
from codebase_rag.graph_updater import MemgraphIngestor
from codebase_rag.config import settings
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console(width=None, force_terminal=True)

async def query(question: str, repo_path: str):
    init_session_log(_setup_common_initialization(repo_path))
    log_session_event(f"USER: {question}")
    with MemgraphIngestor(
        host=settings.MEMGRAPH_HOST,
        port=settings.MEMGRAPH_PORT,
    ) as ingestor:
        console.print("[bold green]Successfully connected to Memgraph.[/bold green]")
        rag_agent = _initialize_services_and_agent(repo_path, ingestor)
        response = await rag_agent.run(question + get_session_context(), message_history=[])
        return response.output


# async def optimize(repo_path: str):
#     target