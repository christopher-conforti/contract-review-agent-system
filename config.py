"""API key and model configuration, shared by all agents."""

import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-opus-4-1-20250805"
MAX_TOKENS = 4096
