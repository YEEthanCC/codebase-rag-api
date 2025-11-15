from codebase_rag.main import run_with_cancellation, _initialize_services_and_agent, _setup_common_initialization, init_session_log, log_session_event, get_session_context
from codebase_rag.graph_updater import MemgraphIngestor
from codebase_rag.config import settings
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console(width=None, force_terminal=True)

def query(question: str, repo_path: str):
    init_session_log(_setup_common_initialization(repo_path))
    log_session_event(f"USER: {question}")
    with MemgraphIngestor(
        host=settings.MEMGRAPH_HOST,
        port=settings.MEMGRAPH_PORT,
    ) as ingestor:
        console.print("[bold green]Successfully connected to Memgraph.[/bold green]")
        rag_agent = _initialize_services_and_agent(repo_path, ingestor)
        response = rag_agent.run(question + get_session_context(), message_history=[])
        return response.output


async def optimize(repo_path: str, language: str, ref: str):
    init_session_log(_setup_common_initialization(repo_path))
    with MemgraphIngestor(
        host=settings.MEMGRAPH_HOST,
        port=settings.MEMGRAPH_PORT,
    ) as ingestor:
        console.print("[bold green]Successfully connected to Memgraph.[/bold green]")

        rag_agent = _initialize_services_and_agent(repo_path, ingestor)
    console.print(
        f"[bold green]Starting {language} optimization session...[/bold green]"
    )
    console.print(
        f"[bold green]Starting {language} optimization session...[/bold green]"
    )
    document_info = (
        f" using the reference document: {ref}"
        if ref
        else ""
    )
    console.print(
        Panel(
            f"[bold yellow]The agent will analyze your codebase{document_info} and propose specific optimizations."
            f" You'll be asked to approve each suggestion before implementation."
            f" Type 'exit' or 'quit' to end the session.[/bold yellow]",
            border_style="yellow",
        )
    )

    # Initial optimization analysis
    instructions = [
        "Use your code retrieval and graph querying tools to understand the codebase structure",
        "Read relevant source files to identify optimization opportunities",
    ]
    if ref:
        instructions.append(
            f"Use the analyze_document tool to reference best practices from {ref}"
        )

    instructions.extend(
        [
            f"Reference established patterns and best practices for {language}",
            "Propose specific, actionable optimizations with file references",
            "IMPORTANT: Do not make any changes yet - just propose them and wait for approval",
            "After approval, use your file editing tools to implement the changes",
        ]
    )
    numbered_instructions = "\n".join(
        f"{i + 1}. {inst}" for i, inst in enumerate(instructions)
    )
    initial_question = f"""
I want you to analyze my {language} codebase and propose specific optimizations based on best practices.

Please:
{numbered_instructions}

Start by analyzing the codebase structure and identifying the main areas that could benefit from optimization.
Remember: Propose changes first, wait for my approval, then implement.
"""
    with console.status(
        "[bold green]Agent is analyzing codebase... (Press Ctrl+C to cancel)[/bold green]"
    ):
        response = await run_with_cancellation(
            console,
            rag_agent.run(
                initial_question + get_session_context(), message_history=[]
            ),
        )

        if isinstance(response, dict) and response.get("cancelled"):
            log_session_event("ASSISTANT: [Analysis was cancelled]")
            session_cancelled = True
    return response.output