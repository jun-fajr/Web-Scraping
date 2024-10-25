import os
import markdown
import pdfkit

# Folder tempat file .md berada
input_folder = 'chapters_output'
# Folder tempat file .pdf disimpan (ubah sesuai keinginan Anda)
output_folder = 'pdf_output'

# Pastikan folder output ada
os.makedirs(output_folder, exist_ok=True)

# CSS untuk styling PDF
custom_css = """
<style>
    body {
        font-family: Arial, sans-serif;
        font-size: 14pt;  /* Meningkatkan ukuran font */
        line-height: 1.6;
        margin: 20px;
        color: #333;
    }
    h1, h2, h3, h4 {
        color: #2c3e50;
    }
    pre {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        padding: 10px;
        overflow-x: auto;
    }
</style>
"""

# Fungsi untuk mengganti karakter tidak valid
def clean_text(text):
    replacements = {
        'â€œ': '“',  # Ganti dengan tanda kutip pembuka
        'â€': '”',   # Ganti dengan tanda kutip penutup
        # Tambahkan lebih banyak penggantian jika perlu
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# Loop melalui semua file .md di folder input
for filename in os.listdir(input_folder):
    if filename.endswith('.md'):
        # Baca file .md
        md_file_path = os.path.join(input_folder, filename)
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Bersihkan konten dari karakter yang tidak valid
        md_content = clean_text(md_content)

        # Konversi ke HTML
        html_content = markdown.markdown(md_content)

        # Tambahkan CSS ke HTML
        full_html_content = f"<html><head>{custom_css}</head><body>{html_content}</body></html>"

        # Tentukan nama file PDF
        pdf_filename = filename.replace('.md', '.pdf')
        pdf_file_path = os.path.join(output_folder, pdf_filename)

        # Konversi HTML ke PDF
        try:
            pdfkit.from_string(full_html_content, pdf_file_path, options={"encoding": "UTF-8"})
            print(f"Converted {filename} to {pdf_filename}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")

print("Semua file .md telah dikonversi menjadi PDF!")
