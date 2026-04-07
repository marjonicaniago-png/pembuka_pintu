# Gunakan mesin dasar Python yang ringan
FROM python:3.9-slim

# Perintahkan mesin Linux mengunduh dan memasang Java (JRE)
RUN apt-get update && \
    apt-get install -y default-jre && \
    rm -rf /var/lib/apt/lists/*

# Atur folder kerja
WORKDIR /app

# Salin semua file dari GitHub ke dalam mesin
COPY . /app

# Pasang pustaka Python
RUN pip install --no-cache-dir -r requirements.txt

# Buka jalur komunikasi di port 5000
EXPOSE 5000

# Perintah utama untuk menyalakan server menggunakan Gunicorn (Standar Produksi)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
