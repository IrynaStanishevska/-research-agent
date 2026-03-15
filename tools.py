from pathlib import Path
from urllib.parse import urlparse

import trafilatura
from ddgs import DDGS
from langchain.tools import tool

from config import Settings

settings = Settings()


def _truncate(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n\n[Truncated]"


@tool
def write_report(filename: str, content: str) -> str:
    """
    Save the final Markdown report to a file in the output directory.
    Returns a confirmation message with the saved file path.
    """
    try:
        output_dir = Path(settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = Path(filename).name
        if not safe_name.endswith(".md"):
            safe_name += ".md"

        file_path = output_dir / safe_name
        file_path.write_text(content, encoding="utf-8")

        return f"Report saved to: {file_path.resolve()}"
    except Exception as e:
        return f"Error writing report: {e}"


@tool
def web_search(query: str) -> list[dict]:
    """
    Search the web using DuckDuckGo and return a short list of results.
    Each result contains title, url, and snippet.
    """
    try:
        results = list(DDGS().text(query, max_results=settings.max_search_results))

        formatted_results = []
        total_chars = 0
        max_total_chars = 4000

        for item in results:
            result = {
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
            }

            result_text = f"{result['title']} {result['url']} {result['snippet']}"
            total_chars += len(result_text)

            if total_chars > max_total_chars:
                break

            formatted_results.append(result)

        if not formatted_results:
            return [{"error": "No search results found."}]

        return formatted_results
    except Exception as e:
        return [{"error": f"Web search failed: {e}"}]


@tool
def read_url(url: str) -> str:
    """
    Read the main text content from a webpage URL and return truncated text.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return "Error: Invalid URL. URL must start with http:// or https://"

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return "Error: Failed to download the page."

        text = trafilatura.extract(downloaded)
        if not text:
            return "Error: Could not extract readable text from the page."

        return _truncate(text, settings.max_url_content_length)
    except Exception as e:
        return f"Error reading URL: {e}"