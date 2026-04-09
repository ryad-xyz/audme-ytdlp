from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({
    "status": "online",
    "message": "Server yt-dlp Papah Siap Mengekstrak Data!"
  })

@app.route('/api/extract')
def extract_data():
  # URL bisa berupa link video tunggal, link playlist, atau link channel
  url = request.args.get('url')
  
  if not url:
    return jsonify({"error": "Parameter 'url' wajib diisi"}), 400

  # Konfigurasi sakti untuk yt-dlp di Vercel (Serverless)
  ydl_opts = {
    'quiet': True,             # Jangan tampilkan log di console
    'skip_download': True,     # PENTING: Jangan download videonya!
    'extract_flat': True,      # Jika URL berupa channel/playlist, cukup ambil judul & ID-nya saja agar cepat
    'no_cache_dir': True,      # Mencegah error folder Read-Only di Vercel
    'format': 'bestaudio/best' # Persiapan jika papah mau ambil URL mentah (raw audio stream)
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # Jalankan proses ekstraksi metadata
      info = ydl.extract_info(url, download=False)
      
      # Menghilangkan beberapa properti bawaan yt-dlp yang terlalu panjang (opsional)
      if 'formats' in info and ydl_opts.get('extract_flat'):
         del info['formats']

      return jsonify({
        "status": "success",
        "data": info
      })
      
  except Exception as e:
    return jsonify({
      "status": "error",
      "message": str(e)
    }), 500

# Wajib ada agar dibaca oleh Vercel