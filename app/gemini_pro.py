"""Gemini Pro: narration + dialogue for each panel."""
import re

from app import config


def _demo_story(outline, character, tone):
    parts = []
    for p in outline:
        parts.append(
            f"Panel {p['panel']}:\nCaption: {p['title']}.\n"
            f"Narration: {p['scene']}\n{character}: \"This is going to be {tone}!\""
        )
    return "\n\n".join(parts)


def generate_story(outline, character, tone):
    if not config.TEXT_LIVE:
        return _demo_story(outline, character, tone)

    import google.generativeai as genai

    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    panels = "\n".join(f"Panel {p['panel']} - {p['title']}: {p['scene']}" for p in outline)
    instruction = (
        f"Write comic narration and character dialogue in a {tone} tone for these panels. "
        f"Main character: {character}.\n{panels}\n"
        "Format exactly as blocks starting with 'Panel N:' then 'Caption:' and 'Narration:' lines."
    )
    return model.generate_content(instruction).text


def split_story(story, count):
    """Split the full story text into a list of per-panel strings."""
    chunks = re.split(r"(?im)^\s*\**panel\s*\d+\**\s*[:\-]?\s*", story)
    chunks = [c.strip() for c in chunks if c.strip()]
    while len(chunks) < count:
        chunks.append("")
    return chunks[:count]
