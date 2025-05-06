"""
Module for generating visual prompts for TikTok videos.
"""

import json
from pathlib import Path
from typing import Dict, List

from openai import OpenAI


def generate_visual_prompts(
    client: OpenAI, topic: str, output_dir: Path
) -> List[Dict[str, str]]:
    """
    Generate visual prompts for a selected topic using OpenAI API.

    Args:
        client: OpenAI client instance
        topic: The selected tech historical event/topic
        output_dir: Directory to save the prompts

    Returns:
        List of dicts with 'moment' and 'prompt' keys
    """
    print(f"Generating visual prompts for: {topic}")

    prompt = f"""
    I will go with video idea: "{topic}".
    
    Now I need to create visuals for my TikTok. From here you are my new prompt expert and you're going
    to help me create prompts I can use in Leonardo AI to generate my visuals.
    
    What I want you to do is to give me five key moments of the {topic} event/period, describing the
    person whose day we're following (a developer, engineer, executive, or other relevant person). 
    To each of these moments I want you to create an image prompt.
    
    These image prompts will be descriptions of POV images, images from the perspective of the person
    we're following living through this tech-related event.
    
    For each moment, provide:
    1. A brief description of the moment
    2. A detailed prompt for Leonardo AI that includes visual details, style guidance, and POV framing
    
    Return your response as a JSON object with a key called "prompts" that contains an array of objects with 'moment' and 'prompt' keys.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    # Extract and parse JSON from the response
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        prompts = data.get("prompts", [])

        # Save prompts to file
        if prompts:
            topic_filename = topic.replace("/", "-").replace(" ", "_")[:50]
            with open(output_dir / f"{topic_filename}_prompts.json", "w") as f:
                json.dump(prompts, f, indent=2)

        return prompts
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw response: {content[:200]}...")
        return []
