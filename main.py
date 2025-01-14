import requests
from bs4 import BeautifulSoup
import os

# Buat folder untuk menyimpan chapter jika belum ada
folder = "chapters"
os.makedirs(folder, exist_ok=True)

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
            # Ambil semua elemen <p> dalam chapter_content
            paragraphs = chapter_content.find_all("p")
            
            # Mengubah konten menjadi string markdown
            formatted_paragraphs = []
            for p in paragraphs:
                # Ambil teks dari setiap paragraf
                formatted_paragraphs.append(p.get_text(strip=True))
            
            # Menggabungkan paragraf dengan dua baris kosong
            md_content = "\n\n".join(formatted_paragraphs)
            
            # Ubah judul menjadi format Markdown (# Header)
            md_title = f"# {chapter_title}\n\n"
            
            # Simpan ke file dengan ekstensi .md
            file_path = os.path.join(folder, f"{chapter_title}.md")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(md_title + md_content)  # Tambahkan judul dan isi
            
            print(f"Saved: {file_path}")
        else:
            print(f"Failed to extract content for chapter {chapter_num}")
    else:
        print(f"Chapter {chapter_num} not found, status code: {response.status_code}")

print("Semua chapter telah diunduh dengan format Markdown yang lebih baik!")
