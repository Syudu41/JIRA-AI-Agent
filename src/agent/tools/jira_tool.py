# src/agent/tools/jira_tool.py
from __future__ import annotations
from dataclasses import dataclass
import base64
import requests

@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str

class JiraError(Exception):
    pass

class JiraTool:
    """
    Deterministic tool for JIRA actions.
    Step 1: read-only fetch of issue fields (summary, description).
    """

    def __init__(self, config: JiraConfig):
        self.base_url = config.base_url
        self.email = config.email
        self.api_token = config.api_token
        self._session = requests.Session()
        # Auth is Basic <base64(email:token)>
        token_bytes = f"{self.email}:{self.api_token}".encode("utf-8")
        self._session.headers.update({
            "Authorization": f"Basic {base64.b64encode(token_bytes).decode('utf-8')}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_issue(self, issue_key: str) -> dict:
        """
        Fetch the raw issue JSON. Raises JiraError on HTTP failures.
        """
        url = self._url(f"/rest/api/3/issue/{issue_key}")
        resp = self._session.get(url, timeout=20)
        if not resp.ok:
            raise JiraError(f"GET {url} failed: {resp.status_code} {resp.text[:300]}")
        return resp.json()

    def get_issue_fields(self, issue_key: str) -> dict:
        """
        Return a small, clean payload with summary and description (if present).
        """
        issue = self.get_issue(issue_key)
        fields = issue.get("fields", {}) or {}
        # JIRA Cloud often stores description in Atlassian document format ("content" array)
        # We’ll normalize to plain text best-effort for display purposes.
        summary = fields.get("summary", "")
        description = fields.get("description")

        def atlassian_doc_to_text(node) -> str:
            # Very simple best-effort flattener for Step 1 (good enough to inspect current content).
            # We’ll keep it conservative to avoid surprises.
            if node is None:
                return ""
            if isinstance(node, str):
                return node
            if isinstance(node, dict):
                ntype = node.get("type")
                if ntype == "text":
                    return node.get("text", "")
                parts = []
                for child in node.get("content", []) or []:
                    parts.append(atlassian_doc_to_text(child))
                if ntype in {"paragraph", "heading", "bulletList", "orderedList"}:
                    return "\n".join(p for p in parts if p)
                return "".join(parts)
            if isinstance(node, list):
                return "\n".join(atlassian_doc_to_text(c) for c in node if c)
            return ""

        description_text = ""
        if isinstance(description, dict):
            description_text = atlassian_doc_to_text(description).strip()
        elif isinstance(description, str):
            description_text = description.strip()

        return {
            "key": issue.get("key"),
            "summary": summary,
            "description_text": description_text,
            "raw": issue,  # included for debugging now; don’t log this in prod
        }
