import os
import json
from pathlib import Path

# Dossiers à explorer
BASE_DIR = Path(__file__).resolve().parent.parent
SITES_DIR = BASE_DIR / "sites"
PDF_DIR = BASE_DIR / "plaquettes"
HTML_PLAQUETTES_DIR = BASE_DIR / "html_plaquettes"
INDEX_HTML = BASE_DIR / "index.html"

# Étape 1 : extraire les noms de produit à partir des fichiers
products = set()

for folder in [SITES_DIR, PDF_DIR, HTML_PLAQUETTES_DIR]:
    if folder.exists():
        for file in folder.iterdir():
            if file.is_file():
                products.add(file.stem.lower())

sorted_products = sorted(products)

# Étape 2 : lire index.html et remplacer la ligne const products = [...]
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "const products = ["
start_idx = content.find(start_tag)

if start_idx == -1:
    raise Exception("❌ Ligne 'const products = [' non trouvée dans index.html")

end_idx = content.find("];", start_idx)
if end_idx == -1:
    raise Exception("❌ Fin de tableau '];' non trouvée dans index.html")

# Générer le nouveau tableau JS
product_list_str = ", ".join(f'"{name}"' for name in sorted_products)
new_line = f'{start_tag}{product_list_str}];'

# Étape 3 : remplacer et sauvegarder
new_content = content[:start_idx] + new_line + content[end_idx + 2:]

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"✅ Fichier index.html mis à jour avec {len(sorted_products)} produits.")