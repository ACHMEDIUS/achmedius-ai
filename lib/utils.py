"""
Utility functions for the Achmedius AI automation.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def setup_environment() -> tuple[OpenAI, Path]:
    """
    Set up the environment for the application.

    Returns:
        Tuple containing the OpenAI client and output directory path
    """
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Please add it to your .env file.")

    # Set up OpenAI client
    client = OpenAI(api_key=api_key)

    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    return client, output_dir


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Sanitize a string to be used as a filename.

    Args:
        text: The text to sanitize
        max_length: Maximum length of the resulting filename

    Returns:
        Sanitized filename string
    """
    # Replace problematic characters
    safe_text = text.replace("/", "-").replace("\\", "-")
    safe_text = safe_text.replace(" ", "_").replace(":", "_")

    # Truncate if needed
    return safe_text[:max_length]
