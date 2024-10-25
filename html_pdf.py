import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pdfkit
import time

# Konfigurasi Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Jalankan di background (tanpa GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Ganti path ke chromedriver Anda
service = Service(executable_path='path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL halaman yang ingin diunduh
url = "https://mgkomik.id/komik/master-of-gu/chapter-01/"

# Membuat folder output
output_folder = "html-to-pdf"
os.makedirs(output_folder, exist_ok=True)

# Ambil konten halaman
driver.get(url)

# Tunggu beberapa detik untuk memastikan halaman sepenuhnya dimuat
time.sleep(5)

# Mencari judul dan konten chapter
chapter_title = driver.find_element(By.TAG_NAME, "h1").text.strip()
chapter_content = driver.find_element(By.CLASS_NAME, "entry-content")

# Pastikan konten ditemukan
if chapter_content:
    # Mengambil teks konten
    paragraphs = chapter_content.find_elements(By.TAG_NAME, "p")
    content_text = "\n\n".join([p.text.strip() for p in paragraphs])

    # Membuat HTML untuk PDF
    full_html_content = f"""
    <html>
    <head>
        <title>{chapter_title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.6;
                margin: 20px;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        <h1>{chapter_title}</h1>
        <p>{content_text.replace("\n", "<br>")}</p>
    </body>
    </html>
    """

    # Menyimpan ke file PDF di folder output
    pdf_file_path = os.path.join(output_folder, f"{chapter_title}.pdf")
    pdfkit.from_string(full_html_content, pdf_file_path)

    print(f"Saved: {pdf_file_path}")
else:
    print("Konten chapter tidak ditemukan.")

# Tutup driver
driver.quit()
