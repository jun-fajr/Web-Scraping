import os
import markdown
import pdfkit
import re

# Folder tempat file .md berada
input_folder = 'chapters'
# Folder tempat file .pdf disimpan
output_folder = 'manhua'

# Pastikan folder output ada
os.makedirs(output_folder, exist_ok=True)

# CSS untuk styling PDF
custom_css = """
<style>
    body {
        font-family: Arial, sans-serif;
        font-size: 14pt;  /* Ukuran font yang lebih besar */
        line-height: 1.6;
        margin: 20px;
        color: #333;
    }
    h1 {
        color: #2c3e50;
        font-size: 24pt;  /* Ukuran font untuk judul bab */
        text-align: center;
        margin: 20px 0;
        border-bottom: 2px solid #2c3e50;
    }
    h2, h3 {
        color: #34495e;
        font-size: 20pt;  /* Ukuran font untuk subjudul */
        margin-top: 30px;
    }
    p {
        margin: 10px 0;  /* Margin antara paragraf */
    }
    pre {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        padding: 10px;
        overflow-x: auto;
    }
    hr {
        border: 1px solid #2c3e50; /* Garis pemisah */
        margin: 40px 0; /* Jarak sebelum dan sesudah garis */
    }
</style>
"""

# Mendapatkan semua file .md dan mengekstrak nomor chapter
md_files = [
    f for f in os.listdir(input_folder) if f.endswith('.md')
]

# Mengurutkan file berdasarkan nomor chapter
md_files.sort(key=lambda f: int(re.search(r'(\d+)', f).group()))

for filename in md_files:
    # Baca file .md dengan encoding UTF-8
    md_file_path = os.path.join(input_folder, filename)
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Ganti karakter aneh yang mungkin muncul
    md_content = md_content.replace('â€œ', '“').replace('â€', '”')

    # Konversi ke HTML
    html_content = markdown.markdown(md_content)

    # Tambahkan CSS ke HTML
    full_html_content = f"<html><head>{custom_css}</head><body>{html_content}</body></html>"

    # Ekstrak nomor chapter dari nama file
    chapter_number = re.search(r'(\d+)', filename).group()

    # Tentukan nama file PDF dengan urutan chapter
    pdf_filename = f"{chapter_number}.pdf"  # Menggunakan nomor chapter
    pdf_file_path = os.path.join(output_folder, pdf_filename)

    # Konversi HTML ke PDF
    pdfkit.from_string(full_html_content, pdf_file_path)

    print(f"Converted {filename} to {pdf_filename}")
