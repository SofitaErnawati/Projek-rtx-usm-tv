import feedparser
import re
import cloudscraper
import config

def is_informative_title(title):
    if '?' in title or '!' in title:
        return False
        
    title_lower = title.lower()
    
    if re.match(r'^\d+\s+(ide|cara|fakta|tips|alasan|potret|langkah|rekomendasi|hal)\b', title_lower):
        return False

    blacklisted_phrases = [
        "jelaskan maksud", "beri penjelasan", "buka suara", 
        "angkat bicara", "hasil pertandingan", "rupiah menguat", "rupiah melemah", 
        "baca selengkapnya", "lihat selengkapnya", "cek disini", "baca juga", 
        "ini dia", "seperti ini", "kaya gini", "bikin geger", "penjelasan resmi",
        "video ungkap", "video:", "foto:", "infografis:", "ini daftar", "perbedaan",
        "babak belur"
    ]
    for phrase in blacklisted_phrases:
        if phrase in title_lower:
            return False

    blacklisted_words = [
        "simak", "intip", "begini", "ternyata", "fakta", "wow", "potret", "detik-detik",
        "berikut", "cara", "tips", "trik", "daftar", "rincian", "jadwal", "link", "unduh",
        "video", "foto", "segini", "sinopsis", "hikmah", "jejak", "profil", "rekomendasi",
        "review", "alasan", "makna", "arti", "deretan", "sejarah", "mengenal", "mitos",
        "kumpulan", "pesona", "gaya", "sosok", "bocoran", "terkuak", "menengok",
        "popularitas", "soroti", "skincare", "penjualan", "promo", "tanggapi",
        "melirik", "menikmati", "heboh", "viral", "geger", "gempar",
        "momen", "vs", "klasemen", "skor", "prediksi", "ihsg", "saham",
        "tantangan", "klarifikasi", "strategi", "penjelasan", "jelaskan", "ungkap",
        "ide", "hampers", "resep", "menu", "inspirasi", "katalog", "diskon", 
        "berkesan", "personal", "curhat",
        "eksplorasi", "ekspresi", "karya", "koleksi", "desainer", "busana", "pameran", "estetika",
        "sah", "tok", "genjot", "meladeni", "ambrol", "ambruk", "terciduk", "kepergok",
        "nyungsep", "nongkrong", "ngeri"
    ]
    
    for word in blacklisted_words:
        if re.search(r'\b' + word + r'\b', title_lower):
            return False

    words = title_lower.split()
    for i, word in enumerate(words):
        word_clean = re.sub(r'[^\w\s]', '', word)
        
        if word_clean in ['ini', 'itu']:
            if i > 0:
                prev_word = re.sub(r'[^\w\s]', '', words[i-1])
                allowed_time = ['hari', 'saat', 'tahun', 'bulan', 'minggu', 'pekan', 'kali', 'pagi', 'siang', 'sore', 'malam', 'waktu', 'detik']
                if prev_word not in allowed_time:
                    return False 
            else:
                return False 
                
    words_count = title.split()
    if len(words_count) < 5:
        return False
        
    return True

def clean_prefix(title):
    text = re.sub(r'\[.*?\]|【.*?】|\(.*\)', '', title)
    text = re.sub(r'^[A-Za-z\s]{2,30}\s*-\s+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def paraphrase_title(title):
    replacements = {
        r'\bkena\b': 'terkena',
        r'\bbodoh\b': 'kurang pandai',
        r'\bbikin\b': 'membuat',
        r'\bcuma\b': 'hanya',
        r'\bnumpuk\b': 'menumpuk',
        r'\bkasih\b': 'memberi'
    }
    
    for pattern, replacement in replacements.items():
        title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
        
    return title

def get_news_data(source):
    url = config.RSS_DATABASE.get(source)
    if not url: return []
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        
        if response.status_code != 200:
            return []
            
        feed = feedparser.parse(response.content)
        results = []
        
        for entry in feed.entries:
            judul_asli = entry.title
            
            if is_informative_title(judul_asli):
                judul_bersih = clean_prefix(judul_asli)
                judul_bersih = paraphrase_title(judul_bersih)
                
                if judul_bersih:
                    judul_bersih = judul_bersih[0].upper() + judul_bersih[1:]
                    if judul_bersih.endswith('.'):
                        judul_bersih = judul_bersih[:-1]
                
                waktu_terbit = getattr(entry, 'published', getattr(entry, 'updated', 'Waktu tidak terdeteksi'))
                        
                results.append({
                    "title_display": judul_asli,
                    "title_rtx": judul_bersih,
                    "link": getattr(entry, 'link', '#'),
                    "published": waktu_terbit
                })
            
            if len(results) == 20:
                break
                
        return results
    except Exception:
        return []