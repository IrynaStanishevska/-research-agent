# Research Agent

Research Agent is a tool-based conversational assistant that explores a topic on the web, reads relevant pages, gathers findings, and produces a structured Markdown report.

## Features

- Interactive command-line chat interface
- Multi-step research workflow with tool calling
- Web search via DuckDuckGo
- Full-page content extraction from URLs
- Automatic Markdown report generation
- Configurable model and limits through environment variables
- Session memory for follow-up questions in the same conversation

## Tools

The agent uses three core tools:

- **web_search(query)** — searches the web and returns a short list of relevant results
- **read_url(url)** — extracts the main readable text from a web page
- **write_report(filename, content)** — saves the final Markdown report to a file

## Project Structure

```text
research-agent/
├── main.py
├── agent.py
├── tools.py
├── config.py
├── requirements.txt
├── example_output/
└── README.md