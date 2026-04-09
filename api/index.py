from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({
    "status": "online",
    "message": "RYAD - AUDME!"
  })

@app.route('/api/extract')
def extract_data():
  url = request.args.get('url')
  
  if not url:
    return jsonify({"error": "Parameter 'url' wajib diisi"}), 400

  # KONFIGURASI SAKTI UNTUK BYPASS ANTI-BOT YOUTUBE
  ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'no_cache_dir': True,
    'format': 'bestaudio/best', # Ambil kualitas audio terbaik
    # Ini senjata rahasianya: Menyamar sebagai aplikasi Android & Mobile Web
    'extractor_args': {'youtube': ['player_client=android,mweb']}
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # Jalankan ekstraksi secara penuh untuk mendapatkan raw stream URL
      info = ydl.extract_info(url, download=False)
      
      # Kita filter hasilnya agar JSON tidak kepanjangan dan berat
      # Hanya ambil judul dan URL googlevideo mentahnya saja
      raw_url = info.get('url', None)
      title = info.get('title', 'Unknown Title')

      return jsonify({
        "status": "success",
        "data": {
          "title": title,
          "url": raw_url
        }
      })
      
  except Exception as e:
    return jsonify({
      "status": "error",
      "message": str(e)
    }), 500
