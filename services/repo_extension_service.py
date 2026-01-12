from codebase_rag.graph_updater import MemgraphIngestor
from codebase_rag.config import settings
from rich.console import Console
from rich.prompt import Confirm
from typing import Any
from db.session import get_session, set_session
from ..codebase_rag.tools.codebase_query import create_query_tool
from ..codebase_rag.services.llm import CypherGenerator, create_code_retrieval_tool
from ..codebase_rag.tools.code_retrieval import CodeRetriever, create_code_retrieval_tool
from ..codebase_rag.tools.file_extension_reader import FileExtensionReader, create_file_reader_tool
from ..codebase_rag.tools.file_extension_writer import FileWriter, create_file_writer_tool
from ..codebase_rag.tools.file_extension_editor import FileEditor, create_file_editor_tool
from ..codebase_rag.tools.shell_extension_command import ShellCommander, create_shell_command_tool
from ..codebase_rag.tools.directory_extension_lister import DirectoryLister, create_directory_lister_tool
from ..codebase_rag.tools.document_extension_analyzer import DocumentAnalyzer, create_document_analyzer_tool
from ..codebase_rag.tools.semantic_search import create_semantic_search_tool, create_get_function_source_tool
from ..codebase_rag.services.llm import CypherGenerator, create_rag_orchestrator
from sockets.server import sio

console = Console(width=None, force_terminal=True)
confirm_edits_globally = True

def _initialize_services_and_agent(repo_path: str, ingestor: MemgraphIngestor, socket_id: str) -> Any:
    """Initializes all services and creates the RAG agent."""
    # Validate provider configurations before initializing any LLM services
    from ..codebase_rag.providers import get_provider

    def _validate_provider_config(role: str, config: Any) -> None:
        """Validate a single provider configuration."""
        try:
            provider = get_provider(
                config.provider,
                api_key=config.api_key,
                endpoint=config.endpoint,
                project_id=config.project_id,
                region=config.region,
                provider_type=config.provider_type,
                thinking_budget=config.thinking_budget,
                service_account_file=config.service_account_file,
            )
            provider.validate_config()
        except Exception as e:
            raise ValueError(f"{role.title()} configuration error: {e}") from e

    # Validate both provider configurations
    _validate_provider_config("orchestrator", settings.active_orchestrator_config)
    _validate_provider_config("cypher", settings.active_cypher_config)

    cypher_generator = CypherGenerator()
    code_retriever = CodeRetriever(socket_id=socket_id, ingestor=ingestor)
    file_reader = FileExtensionReader(socket_id=socket_id)
    file_writer = FileWriter(socket_id=socket_id)
    file_editor = FileEditor(socket_id=socket_id)
    shell_commander = ShellCommander(
        project_root='.', 
        timeout=settings.SHELL_COMMAND_TIMEOUT, 
        socket_id=socket_id
    )
    directory_lister = DirectoryLister(project_root=repo_path, socket_id=socket_id)
    document_analyzer = DocumentAnalyzer(project_root=repo_path, socket_id=socket_id)

    query_tool = create_query_tool(ingestor, cypher_generator, console)
    code_tool = create_code_retrieval_tool(code_retriever)
    file_reader_tool = create_file_reader_tool(file_reader)
    file_writer_tool = create_file_writer_tool(file_writer)
    file_editor_tool = create_file_editor_tool(file_editor)
    shell_command_tool = create_shell_command_tool(shell_commander)
    directory_lister_tool = create_directory_lister_tool(directory_lister)
    document_analyzer_tool = create_document_analyzer_tool(document_analyzer)
    semantic_search_tool = create_semantic_search_tool()
    function_source_tool = create_get_function_source_tool()

    rag_agent = create_rag_orchestrator(
        tools=[
            query_tool,
            code_tool,
            file_reader_tool,
            file_writer_tool,
            file_editor_tool,
            shell_command_tool,
            directory_lister_tool,
            document_analyzer_tool,
            semantic_search_tool,
            function_source_tool,
        ]
    )
    return rag_agent


async def query(question: str, repo_path: str, session_id: str):
    console.print("[bold green]Successfully connected to Memgraph.[/bold green]")
    history = get_session(session_id)
    with MemgraphIngestor(
        host=settings.MEMGRAPH_HOST,
        port=settings.MEMGRAPH_PORT,
    ) as ingestor:
        rag_agent = _initialize_services_and_agent(repo_path, ingestor, socket_id=session_id)
        response = await rag_agent.run(question, message_history=history)
        history.extend(response.new_messages())
        set_session(session_id, history)
        return response.output
