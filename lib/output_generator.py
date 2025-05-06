"""
Module for generating instruction files and workflow guides.
"""

from pathlib import Path
from typing import Dict, List


def prepare_leonardo_instructions(
    topic: str, visual_prompts: List[Dict[str, str]], output_dir: Path
) -> str:
    """
    Create instructions file for using Leonardo AI with the generated prompts.

    Args:
        topic: The selected topic
        visual_prompts: List of prompt dictionaries
        output_dir: Directory to save the instructions

    Returns:
        Path to instructions file
    """
    instructions = f"""# Leonardo AI Instructions for "{topic}"

## Settings to Use
- Generation Mode: Text to Image
- Image Aspect Ratio: 9:16 (vertical for TikTok)
- Recommended Style: Photorealistic or Cinematic

## Prompts to Use

"""

    for i, vp in enumerate(visual_prompts, 1):
        instructions += f"### Image {i}: {vp.get('moment', f'Moment {i}')}\n\n"
        instructions += f"```\n{vp.get('prompt', 'No prompt available')}\n```\n\n"

    # Save instructions to file
    topic_filename = topic.replace("/", "-").replace(" ", "_")[:50]
    instructions_file = output_dir / f"{topic_filename}_leonardo_instructions.md"
    with open(instructions_file, "w") as f:
        f.write(instructions)

    return str(instructions_file)


def prepare_workflow_guide(
    topic: str, leonardo_instructions_path: str, output_dir: Path
) -> str:
    """
    Create a workflow guide for the complete video creation process.

    Args:
        topic: The selected topic
        leonardo_instructions_path: Path to Leonardo AI instructions
        output_dir: Directory to save the workflow guide

    Returns:
        Path to workflow guide file
    """
    workflow = f"""# Complete Workflow Guide for "{topic}" TikTok Video

## Step 1: Generate Topic ✅
- Selected topic: {topic}

## Step 2: Generate Visual Prompts ✅
- Visual prompts generated and saved

## Step 3: Generate Visuals in Leonardo AI
1. Go to [Leonardo AI](https://leonardo.ai)
2. Use the instructions in: {leonardo_instructions_path}
3. Settings to use:
   - Generation mode: Text to Image
   - Image aspect ratio: 9:16 (vertical for TikTok)
   - Download all generated images

## Step 4: Animate Images in Runway
1. Go to [Runway](https://runwayml.com)
2. Upload the images from Leonardo AI
3. Use Motion Brush or Gen-2 for animation
4. Export the animated sequences

## Step 5: Edit Video in CapCut
1. Import animated visuals
2. Arrange clips in sequence
3. Add transitions (recommend smooth dissolves)
4. Add captions explaining each moment
5. Add sound effects & background music from Epidemic Sound
   - Consider technology sounds (keyboard typing, startup chimes, etc.)
   - Background music should match the era/feel of the technology event
6. Export in high quality (1080p minimum)

## Notes
- Keep the video between 30-60 seconds
- Focus on the POV perspective in your editing
- Consider adding factual text overlays to provide context
"""

    # Save workflow guide to file
    topic_filename = topic.replace("/", "-").replace(" ", "_")[:50]
    workflow_file = output_dir / f"{topic_filename}_workflow_guide.md"
    with open(workflow_file, "w") as f:
        f.write(workflow)

    return str(workflow_file)
