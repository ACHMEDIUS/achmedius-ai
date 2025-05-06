"""
Module for generating viral tech-related video topics.
"""

import re
from typing import List

from openai import OpenAI


def generate_video_topics(client: OpenAI) -> str:
    """
    Generate a list of 10 interesting tech-related historical events using the OpenAI API.

    Args:
        client: OpenAI client instance

    Returns:
        str: The response from the API containing the list of topics
    """
    prompt = (
        "Can you give me a list of 10 different historical events, periods or crisis "
        "or facts or stories that would be interesting for a person to live through today "
        "but then related to computer science, technology and that sort of stuff. "
        "Some examples could be original apple iphone development, the microsoft vs us "
        "lawsuit or ai chatbots today."
    )
    response = client.chat.completions.create(
        model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def extract_topics(topics_text: str) -> List[str]:
    """
    Extract and clean up topics from the response text.

    Args:
        topics_text: Raw text from the OpenAI API

    Returns:
        List of cleaned topic strings
    """
    # Look for numbered or bullet points or asterisks with bold formatting
    topics = re.findall(r"\*\*(.+?)\*\*", topics_text)

    # If we couldn't find formatted topics, try looking for numbered lists
    if not topics or len(topics) < 5:
        topics = re.findall(
            r"\d+\.\s*(?:\*\*)?([^*\n]+?)(?:\*\*)?(?:\s*-|\s*\(|\s*:)", topics_text
        )

    # Final backup: just split by newlines and clean
    if not topics or len(topics) < 5:
        topics = [
            line.strip()
            for line in topics_text.split("\n")
            if line.strip()
            and not line.strip().startswith("These")
            and len(line.strip()) > 10
        ]

    # Clean up the topics
    topics = [re.sub(r"^[\d\.\s\-*]+", "", topic).strip() for topic in topics]
    topics = [re.sub(r"\s*-.*$", "", topic).strip() for topic in topics]

    return topics
