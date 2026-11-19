"""
Kurulum Kontrol Scripti
========================
Ollama servisine bağlanıp embedding ve sohbet modellerini kısa bir testle dener.
Sonuçları Türkçe olarak terminale yazdırır.

Kullanım:
    python 00_kurulum_kontrol.py
"""

import sys
import requests
from config import OLLAMA_URL, EMBED_MODEL, CHAT_MODEL


def satir_ciz(karakter="─", uzunluk=60):
    print(karakter * uzunluk)


def ollama_baglanti_kontrol():
    """Ollama servisinin çalışıp çalışmadığını kontrol eder."""
    print("\n🔍 Ollama bağlantı kontrolü yapılıyor...")
    satir_ciz()

    try:
        yanit = requests.get(OLLAMA_URL, timeout=5)
        if yanit.status_code == 200:
            print(f"✅ Ollama servisi çalışıyor  →  {OLLAMA_URL}")
            return True
        else:
            print(f"⚠️  Ollama servisinden beklenmeyen yanıt: HTTP {yanit.status_code}")
            return False
    except requests.ConnectionError:
        print(f"❌ Ollama servisine bağlanılamadı!")
        print(f"   Adres: {OLLAMA_URL}")
        print(f"\n   Çözüm önerileri:")
        print(f"   1. Ollama'nın kurulu olduğundan emin olun: https://ollama.com")
        print(f"   2. Ollama'yı başlatın:  ollama serve")
        print(f"   3. .env dosyasında OLLAMA_URL değerini kontrol edin")
        return False
    except requests.Timeout:
        print(f"❌ Ollama servisine bağlantı zaman aşımına uğradı!")
        print(f"   Adres: {OLLAMA_URL}")
        return False


def embedding_testi():
    """Embedding modelini kısa bir metinle test eder."""
    print(f"\n🧮 Embedding modeli test ediliyor: {EMBED_MODEL}")
    satir_ciz()

    test_metni = "Bu bir oltalama tespit sistemi testidir."

    try:
        yanit = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": test_metni},
            timeout=60,
        )

        if yanit.status_code == 200:
            veri = yanit.json()
            embedding = veri.get("embedding", [])
            if embedding:
                print(f"✅ Embedding modeli çalışıyor!")
                print(f"   Model        : {EMBED_MODEL}")
                print(f"   Test metni   : \"{test_metni}\"")
                print(f"   Vektör boyutu: {len(embedding)}")
                print(f"   İlk 5 değer : {embedding[:5]}")
                return True
            else:
                print(f"⚠️  Embedding yanıtı boş döndü.")
                return False
        else:
            hata = yanit.json().get("error", yanit.text)
            print(f"❌ Embedding modeli hatası: {hata}")
            print(f"\n   Model indirmek için:  ollama pull {EMBED_MODEL}")
            return False

    except requests.RequestException as e:
        print(f"❌ Embedding testi sırasında hata: {e}")
        return False


def sohbet_testi():
    """Sohbet modelini kısa bir soru ile test eder."""
    print(f"\n💬 Sohbet modeli test ediliyor: {CHAT_MODEL}")
    satir_ciz()

    test_mesaji = "Merhaba! Tek cümleyle kendini tanıt."

    try:
        yanit = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": CHAT_MODEL,
                "prompt": test_mesaji,
                "stream": False,
            },
            timeout=120,
        )

        if yanit.status_code == 200:
            veri = yanit.json()
            cevap = veri.get("response", "").strip()
            if cevap:
                print(f"✅ Sohbet modeli çalışıyor!")
                print(f"   Model  : {CHAT_MODEL}")
                print(f"   Soru   : \"{test_mesaji}\"")
                print(f"   Yanıt  : \"{cevap[:200]}\"")
                return True
            else:
                print(f"⚠️  Sohbet modeli boş yanıt döndürdü.")
                return False
        else:
            hata = yanit.json().get("error", yanit.text)
            print(f"❌ Sohbet modeli hatası: {hata}")
            print(f"\n   Model indirmek için:  ollama pull {CHAT_MODEL}")
            return False

    except requests.RequestException as e:
        print(f"❌ Sohbet testi sırasında hata: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  🛡️  Oltalama Tespit Sistemi — Kurulum Kontrolü")
    print("=" * 60)

    sonuclar = {}

    # 1) Ollama bağlantı kontrolü
    sonuclar["Ollama Bağlantısı"] = ollama_baglanti_kontrol()

    if not sonuclar["Ollama Bağlantısı"]:
        print("\n❌ Ollama servisi çalışmıyor. Diğer testler atlanıyor.\n")
        sys.exit(1)

    # 2) Embedding modeli testi
    sonuclar["Embedding Modeli"] = embedding_testi()

    # 3) Sohbet modeli testi
    sonuclar["Sohbet Modeli"] = sohbet_testi()

    # Özet
    print("\n")
    satir_ciz("=")
    print("  📋 SONUÇ ÖZETİ")
    satir_ciz("=")
    for ad, durum in sonuclar.items():
        simge = "✅" if durum else "❌"
        print(f"   {simge}  {ad}")
    satir_ciz("=")

    basarisiz = [ad for ad, durum in sonuclar.items() if not durum]
    if basarisiz:
        print(f"\n⚠️  {len(basarisiz)} test başarısız oldu. Yukarıdaki mesajları inceleyin.\n")
        sys.exit(1)
    else:
        print("\n🎉 Tüm kontroller başarılı! Sistem kullanıma hazır.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
