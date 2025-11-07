# scripts/test_jira_fetch.py
import sys
from src.agent.config import get_settings
from src.agent.tools.jira_tool import JiraTool, JiraConfig, JiraError

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_jira_fetch.py <ISSUE_KEY>")
        print("Example: python scripts/test_jira_fetch.py HV-123")
        sys.exit(1)

    issue_key = sys.argv[1]
    settings = get_settings()

    jira = JiraTool(JiraConfig(
        base_url=settings.jira_base_url,
        email=settings.jira_email,
        api_token=settings.jira_api_token,
    ))

    try:
        info = jira.get_issue_fields(issue_key)
    except JiraError as e:
        print(f"[JIRA ERROR] {e}")
        sys.exit(2)

    # Minimal, safe printing (avoid dumping secrets)
    print("----- JIRA ISSUE -----")
    print(f"Key:        {info['key']}")
    print(f"Summary:    {info['summary']}")
    print("Description (plain text best-effort):")
    print("--------------------------------------")
    print(info["description_text"] or "(no description)")
    print("--------------------------------------")

if __name__ == "__main__":
    main()
