from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: SecretStr = Field(alias="OPENAI_API_KEY")
    model_name: str = Field(default="gpt-4o-mini", alias="MODEL_NAME")

    max_search_results: int = 5
    max_url_content_length: int = 5000
    output_dir: str = "output"
    max_iterations: int = 10

    model_config = {
        "env_file": ".env",
        "populate_by_name": True,
    }


SYSTEM_PROMPT = """
You are a research agent.

Your job is to answer the user's question by:
1. searching the web,
2. reading relevant URLs,
3. collecting findings,
4. writing a structured Markdown report.

Guidelines:
- Break the task into multiple research steps.
- Use tools when needed.
- Prefer several relevant sources instead of one.
- If a tool fails, continue with other available information.
- Keep tool usage efficient.
- Produce a clear structured Markdown answer.
- When appropriate, save the final report with write_report.
"""