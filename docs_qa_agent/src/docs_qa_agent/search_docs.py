import re
from collections import Counter
from pathlib import Path

from pydantic import Field

from nat.builder.builder import Builder
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig

TOKEN_RE = re.compile(r"[a-z0-9]+")


class SearchDocsConfig(FunctionBaseConfig, name="search_docs"):
    docs_dir: str = Field(description="Folder containing markdown docs to search.")
    chunk_chars: int = Field(default=800, description="Approximate size of each searchable chunk.")
    top_k: int = Field(default=3, description="Number of chunks returned per search.")


def _chunk_docs(docs_dir: Path, chunk_chars: int) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    for path in sorted(docs_dir.glob("**/*.md")):
        text = path.read_text(encoding="utf-8")
        for start in range(0, len(text), chunk_chars):
            chunks.append((path.name, text[start:start + chunk_chars]))
    return chunks


def _score(query_terms: Counter, chunk: str) -> float:
    chunk_terms = Counter(TOKEN_RE.findall(chunk.lower()))
    return sum(min(count, chunk_terms[term]) for term, count in query_terms.items())


def search_chunks(docs_dir: str, query: str, chunk_chars: int, top_k: int) -> list[dict]:
    query_terms = Counter(TOKEN_RE.findall(query.lower()))
    scored = []
    for source, chunk in _chunk_docs(Path(docs_dir), chunk_chars):
        score = _score(query_terms, chunk)
        if score > 0:
            scored.append({"source": source, "score": score, "text": chunk})
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


@register_function(config_type=SearchDocsConfig)
async def search_docs(config: SearchDocsConfig, builder: Builder):

    async def _search(query: str) -> str:
        """Search the documentation for passages relevant to the query. Returns passages with their source file names."""
        hits = search_chunks(config.docs_dir, query, config.chunk_chars, config.top_k)
        if not hits:
            return "No matching documentation found."
        return "\n\n".join(f"[source: {h['source']}]\n{h['text']}" for h in hits)

    yield FunctionInfo.from_fn(_search, description=_search.__doc__)
