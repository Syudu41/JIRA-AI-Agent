# src/agent/config.py
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from project root

@dataclass
class Settings:
    openai_api_key: str
    openai_model: str
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    tech_stack_field_id: str | None = None  # optional for later

def get_settings() -> Settings:
    missing = []
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    settings = Settings(
        openai_api_key = OPENAI_API_KEY or "",
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        jira_base_url = os.getenv("JIRA_BASE_URL", "").rstrip("/"),
        jira_email = os.getenv("JIRA_EMAIL", ""),
        jira_api_token = os.getenv("JIRA_API_TOKEN", ""),
        tech_stack_field_id = os.getenv("TECH_STACK_FIELD_ID") or None,
    )

    if not settings.jira_base_url: missing.append("JIRA_BASE_URL")
    if not settings.jira_email:    missing.append("JIRA_EMAIL")
    if not settings.jira_api_token:missing.append("JIRA_API_TOKEN")

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return settings
