import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os

# Buat folder untuk menyimpan chapter jika belum ada
folder = "chapters-pdf"
os.makedirs(folder, exist_ok=True)

# Buat kelas PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Chapter", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Loop untuk mengambil chapter dari 1 hingga 2334
for chapter_num in range(1, 2335):  # 2335 karena range di Python eksklusif
    chapter_url = f"https://novelringan.com/reverend-insanity-chapter-{chapter_num}"
    response = requests.get(chapter_url)
    
    # Periksa apakah request berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Coba temukan judul chapter dan konten chapter
        chapter_title = soup.find("h1")
        chapter_content = soup.find("div", {"class": "entry-content"})
        
        # Pastikan elemen ditemukan sebelum menyimpan
        if chapter_title and chapter_content:
            chapter_title = chapter_title.text.strip()
            
            # Mengganti karakter yang tidak valid untuk nama file
            chapter_title = "".join(c for c in chapter_title if c.isalnum() or c in (" ", "-", "_")).rstrip()

            # Membuat file PDF
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Menulis judul chapter
            pdf.cell(0, 10, chapter_title, ln=True, align='C')
            pdf.ln(10)  # Jarak sebelum konten

            # Ambil semua elemen <p> dalam chapter_content
            paragraphs = chapter_content.find_all("p")
            
            # Menulis konten chapter
            for p in paragraphs:
                text = p.get_text(strip=True)

                # Menangani karakter khusus
                text = text.replace('\u2013', '-')  # Mengganti en dash dengan tanda hubung
                text = text.replace('\u2014', '-')  # Mengganti em dash dengan tanda hubung
                text = text.replace('\u2018', "'")   # Mengganti tanda kutip tunggal kiri
                text = text.replace('\u2019', "'")   # Mengganti tanda kutip tunggal kanan
                text = text.replace('\u201c', '"')   # Mengganti tanda kutip ganda kiri
                text = text.replace('\u201d', '"')   # Mengganti tanda kutip ganda kanan
                text = text.replace('\u2026', '...')  # Mengganti elipsis

                # Menulis setiap paragraf ke PDF
                pdf.multi_cell(0, 10, text)
                pdf.ln(5)  # Jarak antar paragraf

            # Simpan ke file PDF
            pdf_file_path = os.path.join(folder, f"{chapter_num:04d} - {chapter_title}.pdf")  # Menyimpan dengan format nomor chapter
            
            try:
                pdf.output(pdf_file_path)
                print(f"Saved: {pdf_file_path}")
            except Exception as e:
                print(f"Failed to save {pdf_file_path}: {e}")
        else:
            print(f"Failed to extract content for chapter {chapter_num}")
    else:
        print(f"Chapter {chapter_num} not found, status code: {response.status_code}")

print("Semua chapter telah diunduh dalam format PDF!")
