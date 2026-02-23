from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    output_image = remove(input_image)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")