from app.gemini_pro import split_story


def build_comic_layout(outline, image_paths, story):
    texts = split_story(story, len(outline))
    return [
        {
            "panel": p["panel"],
            "title": p["title"],
            "scene": p["scene"],
            "image_prompt": p["image_prompt"],
            "image": img.replace("\\", "/"),
            "text": txt,
        }
        for p, img, txt in zip(outline, image_paths, texts)
    ]
