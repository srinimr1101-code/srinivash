from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import config
from app.exporters import save_pdf
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.schemas import PromptRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def run_pipeline(prompt, character, setting, tone, style):
    outline = generate_outline(prompt, character, setting, tone, style)
    story = generate_story(outline, character, tone)
    images = [generate_image(p["image_prompt"], p["title"]) for p in outline]
    layout = build_comic_layout(outline, images, story)
    pdf_path = save_pdf(layout)
    return layout, pdf_path


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"demo": not config.TEXT_LIVE})


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    prompt: str = Form(...),
    character: str = Form("Hero"),
    setting: str = Form("forest"),
    tone: str = Form("dramatic"),
    style: str = Form("comic book"),
):
    try:
        layout, pdf_path = run_pipeline(prompt, character, setting, tone, style)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")
    return templates.TemplateResponse(
        request, "comic_preview.html", {"layout": layout, "pdf_path": "/" + pdf_path}
    )


@router.post("/generate-comic/json")
async def generate_json(req: PromptRequest):
    try:
        layout, pdf_path = run_pipeline(req.prompt, req.character, req.setting, req.tone, req.style)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")
    return {"layout": layout, "pdf_path": pdf_path}


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str = ""):
    return templates.TemplateResponse(request, "export_success.html", {"pdf": pdf})


@router.get("/test-image")
async def test_image(prompt: str = "a brave fox in an enchanted forest"):
    return {"image": generate_image(prompt, "Test image")}
