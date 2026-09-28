# ComicCraft – AI Comic Story Creator (Gemini + Stable Diffusion)

FastAPI web app: prompt → 5-panel outline (Gemini Flash) → narration/dialogue (Gemini Pro)
→ panel art (Stable Diffusion) → layout → PDF export.

## Run
Windows: double-click `run.bat`  |  macOS/Linux: `./run.sh`
Or manually:
```
python -m venv env && source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                             # add GEMINI_API_KEY
python run.py                                    # or: uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000  (API docs: /docs)

## Demo mode
With no `GEMINI_API_KEY` the app still runs end to end using sample text and placeholder
art. For real images, uncomment diffusers/transformers/accelerate/torch in requirements.txt.

## Routes
`/` form · `POST /generate` preview · `POST /generate-comic/json` API · `/export-success` · `/test-image`
