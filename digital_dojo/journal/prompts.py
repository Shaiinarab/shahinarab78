import random
from .prompts_data import PHILOSOPHICAL_PROMPTS

def get_random_prompt() -> dict | None:
    """
    Selects and returns one random philosophical prompt.
    Returns:
        A dictionary representing a prompt, or None if the list is empty.
    """
    if not PHILOSOPHICAL_PROMPTS:
        return None
    return random.choice(PHILOSOPHICAL_PROMPTS)

def get_prompt_by_id(prompt_id: str) -> dict | None:
    """
    Searches for a prompt with the given ID.
    Args:
        prompt_id: The unique ID of the prompt.
    Returns:
        The prompt dictionary if found, otherwise None.
    """
    for prompt in PHILOSOPHICAL_PROMPTS:
        if prompt["id"] == prompt_id:
            return prompt
    return None
