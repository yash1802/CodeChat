"""
Giving a specific role to an LLM through a system prompt (in this case, a senior software engineer at big tech) improves the quality of the LLM's 
response - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
"""

SYSTEM_PROMPT = ("You are a senior software engineer at a big tech company and you possess a PhD in Computer Science from MIT."
                "We need your help in understanding a code repository, answer any questions that we may have."
                "Following this, I will provide the full code repository, represented in XML format.")

INITIAL_USER_QUERY = "Give a brief summary of the code."

DOCUMENT_GENERATION_QUERY = ("Generate documentation for the code that was shared with you. "
                             "Include the following: Summary of the code, directory structure and one-liner description of each file, requirements, running instructions. "
                             "If the codebase already has documentation (README), don't generate anything and instead, inform the user of the existing document.")

ISSUE_INVESTIGATION_PROMPT = ("We have an issue open on github related to the code that was shared with you."
                              "Help us understand said issue: describe it in detail, analyse the reason for it and then suggest ways to resolve it."
                              "Following this, the issue in question is shared, represented as XML.")

CLAUDE_API_KEY = "Enter your Claude API key"

