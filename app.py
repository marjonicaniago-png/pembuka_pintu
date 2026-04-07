import os
import subprocess
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ API Mesin Dekompilator Berjalan Sempurna!"

@app.route('/unluac', methods=['POST'])
def decompile_lua():
    try:
        # 1. Menangkap data bytecode dari skrip Jieshuo
        encoded_data = request.form.get('file_bytecode')
        if not encoded_data:
            return "ERROR: Payload bytecode tidak ditemukan", 400

        # 2. Decode Base64 kembali ke format biner murni
        # Kita perbaiki spasi yang mungkin berubah menjadi '+' saat pengiriman HTTP
        encoded_data = encoded_data.replace(' ', '+')
        bytecode = base64.b64decode(encoded_data)

        # 3. Simpan biner sementara di server
        temp_file = "temp_target.luac"
        with open(temp_file, "wb") as f:
            f.write(bytecode)

        # 4. Eksekusi file Java unluac.jar untuk membedah biner
        # Pastikan unluac.jar ada di folder yang sama
        cmd = ["java", "-jar", "unluac.jar", temp_file]
        
        # Proses eksekusi dengan batas waktu (timeout) 10 detik
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        # 5. Hapus file biner sementara agar server tetap bersih
        if os.path.exists(temp_file):
            os.remove(temp_file)

        # 6. Kirim hasil kembali ke Jieshuo
        if result.returncode == 0 and result.stdout:
            return result.stdout, 200
        else:
            return f"ERROR_DECOMPILER: {result.stderr}", 500

    except subprocess.TimeoutExpired:
        return "ERROR: Proses dekompilasi terlalu lama (Timeout)", 504
    except Exception as e:
        return f"ERROR_SERVER: {str(e)}", 500

if __name__ == '__main__':
    # Berjalan di port dinamis sesuai pengaturan Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
