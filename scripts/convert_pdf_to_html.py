import os
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "plaquettes"
HTML_OUTPUT_DIR = BASE_DIR / "html_plaquettes"

HTML_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 150  

def convert_pdf_to_html(pdf_path: Path):
    product_name = pdf_path.stem
    output_image_name = f"{product_name}.png"
    output_image_path = HTML_OUTPUT_DIR / output_image_name
    output_html_path = HTML_OUTPUT_DIR / f"{product_name}.html"

    try:
        image = convert_from_path(str(pdf_path), dpi=DPI)[0]  
        image.save(output_image_path, "PNG")
    except Exception as e:
        print(f"❌ Erreur de conversion {pdf_path.name}: {e}")
        return

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>{product_name}</title>
  <style>
    body {{
      margin: 0;
      padding: 2rem;
      background-color: #f4f4f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }}
    .card {{
      background: white;
      border-radius: 12px;
      padding: 1rem;
      box-shadow: 0 6px 12px rgba(0,0,0,0.1);
      max-width: 900px;
      width: 90%;
    }}
    .card img {{
      width: 100%;
      border-radius: 8px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="card">
    <img src="{output_image_name}" alt="{product_name}">
  </div>
</body>
</html>"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ {product_name}.html généré.")

for pdf_file in PDF_DIR.glob("*.pdf"):
    convert_pdf_to_html(pdf_file)