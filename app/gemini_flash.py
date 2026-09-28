"""Gemini Flash: fast structured 5-panel outline."""
import json
import re

from app import config

PANEL_TITLES = ["The Beginning", "Into the Unknown", "The Challenge", "The Turning Point", "A New Dawn"]


def _demo_outline(prompt, character, setting, tone, style):
    beats = [
        f"{character} is introduced in the {setting}, ready for adventure.",
        f"{character} ventures deeper into the {setting} and finds a strange clue.",
        f"A {tone} obstacle blocks {character}'s path.",
        f"{character} finds a clever way through the trouble.",
        f"{character} succeeds and looks toward the horizon.",
    ]
    return [
        {
            "panel": i + 1,
            "title": PANEL_TITLES[i],
            "scene": beats[i],
            "image_prompt": f"{style} illustration, {beats[i]} Story: {prompt}. Mood: {tone}.",
        }
        for i in range(5)
    ]


def generate_outline(prompt, character, setting, tone, style):
    if not config.TEXT_LIVE:
        return _demo_outline(prompt, character, setting, tone, style)

    import google.generativeai as genai

    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    instruction = (
        f"Create a {config.NUM_PANELS}-panel comic outline. Story idea: {prompt}. "
        f"Main character: {character}. Setting: {setting}. Tone: {tone}. Art style: {style}.\n"
        "Return ONLY a JSON array. Each item has keys: panel (int), title, scene, image_prompt."
    )
    text = model.generate_content(instruction).text
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return _demo_outline(prompt, character, setting, tone, style)
    return data[: config.NUM_PANELS]
