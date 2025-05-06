"""
Main entry point for the Achmedius AI video generation automation.
"""

import json
import sys
from pathlib import Path

from lib import output_generator, prompt_generator, topic_generator, utils


def main() -> None:
    """
    Main entry point for the automation script.
    """
    # Setup environment
    client, output_dir = utils.setup_environment()

    print("Step 1: Generating tech-related viral video topics...")

    # Generate video topics
    topics_text = topic_generator.generate_video_topics(client)
    print(topics_text)

    # Extract topics from the response text
    topics = topic_generator.extract_topics(topics_text)

    # Save topics to file
    with open(output_dir / "topics.json", "w") as f:
        json.dump(topics, f, indent=2)

    # Display the extracted topics
    print("\nExtracted Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")

    # Automatically select the first topic for demonstration
    # or let user select if running interactively
    if sys.stdin.isatty():  # Check if running interactively
        print(
            "\nSelect a topic by entering its number (or press Enter to use the first one):"
        )
        try:
            selection = input("\nYour selection (1-10): ")
            index = int(selection) - 1 if selection.strip() else 0
            if index < 0 or index >= len(topics):
                print("Invalid selection, using the first topic")
                index = 0
        except (ValueError, IndexError):
            print("Invalid input, using the first topic")
            index = 0
    else:
        index = 0

    selected_topic = topics[index]
    print(f"\nSelected topic: {selected_topic}")

    # Generate visual prompts for the selected topic
    print("\nStep 2: Generating visual prompts...")
    visual_prompts = prompt_generator.generate_visual_prompts(
        client, selected_topic, output_dir
    )

    if visual_prompts:
        print(f"Generated {len(visual_prompts)} visual prompts.")

        # Step 3: Prepare instructions for Leonardo AI
        leonardo_instructions_path = output_generator.prepare_leonardo_instructions(
            selected_topic, visual_prompts, output_dir
        )
        print(
            f"\nStep 3: Leonardo AI instructions saved to {leonardo_instructions_path}"
        )

        # Create a complete workflow guide
        workflow_guide_path = output_generator.prepare_workflow_guide(
            selected_topic, leonardo_instructions_path, output_dir
        )
        print(f"\nComplete workflow guide saved to {workflow_guide_path}")

        print("\nVisual prompts:")
        for i, prompt in enumerate(visual_prompts, 1):
            moment = prompt.get("moment", "No moment description")
            prompt_text = prompt.get("prompt", "No prompt available")
            print(f"\nPrompt {i}:")
            print(f"Moment: {moment}")
            print(f"Prompt: {prompt_text[:100]}...")
    else:
        print("Failed to generate visual prompts.")


if __name__ == "__main__":
    main()
