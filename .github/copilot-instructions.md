# JIRA AI Agent - Developer Instructions

This document provides essential context for AI agents working with this codebase.

## Project Overview

This is a Python-based JIRA AI Agent that uses OpenAI's API to automatically process and enhance JIRA issues. The agent reads issue summaries and generates structured specifications including descriptions and technology stacks.

## Key Components

### Core Dependencies
- OpenAI API (GPT-4) for AI processing
- JIRA Cloud API (v3) for issue management
- Python packages: `openai`, `python-dotenv`, `requests`
- Optional: `jira` or `atlassian-python-api` for simplified JIRA integration

### Authentication
- Uses Basic Auth with email + API token for JIRA
- OpenAI API key for AI integration
- All credentials managed via environment variables:
  ```
  OPENAI_API_KEY=...
  JIRA_BASE_URL=https://your-domain.atlassian.net
  JIRA_EMAIL=you@company.com
  JIRA_API_TOKEN=...
  ```

## Key Workflows

### Issue Processing Flow
1. Fetch issue summary from JIRA via `GET /rest/api/3/issue/{key}`
2. Process with OpenAI using structured JSON output schema
3. Convert generated content to JIRA's ADF format
4. Update issue via `PUT /rest/api/3/issue/{key}`

### Development Workflow
1. Set up environment variables (never commit `.env`)
2. Use dry-run mode for testing changes
3. Test with sandbox issues before production
4. Monitor for human re-edits to measure quality

## Project-Specific Conventions

### Content Formatting
- JIRA descriptions use Atlassian Document Format (ADF) in Cloud
- Markdown content must be converted to ADF before updating issues
- Use structured JSON schema for OpenAI outputs to ensure consistency

### Error Handling
- Check for 401 errors (auth issues) and 404 errors (missing fields)
- Validate all API responses
- Log all issue updates with before/after states

### Security Practices
- Use least-privilege JIRA bot accounts
- Rotate API tokens regularly
- Implement dry-run mode for human approval
- Add length caps and schema validation for AI outputs

## Integration Points

### External Services
- JIRA Cloud API v3
- OpenAI GPT-4 API

### Cross-Component Communication
- JIRA <-> Python Agent: REST API calls
- Agent <-> OpenAI: Structured JSON responses
- Optional: MCP architecture for modular tool integration

## File Structure
- `.env`: Environment variables (gitignored)
- `extra.txt`: Additional documentation and setup instructions

## Common Issues & Solutions

1. **401 Unauthorized**: Check email/token pair and Cloud base URL
2. **404 on Updates**: Verify API path and field existence in project
3. **Description Not Rendering**: Ensure proper Markdown to ADF conversion