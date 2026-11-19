# 🛡️ Oltalama (Phishing) Tespit Sistemi

> **⚠️ Bu proje yalnızca savunma amaçlıdır.**
> Oltalama saldırılarını **tespit etmek, analiz etmek ve önlemek** için geliştirilmiştir.
> Saldırı amaçlı kullanımı kesinlikle yasaktır ve geliştiricinin sorumluluğunda değildir.

## 🎯 Proje Amacı

E-posta ve URL tabanlı oltalama (phishing) girişimlerini yapay zekâ destekli yöntemlerle tespit eden, analiz eden ve raporlayan bir savunma sistemi geliştirmek.

### Kapsam

| Bileşen | Açıklama |
|---------|----------|
| **ML Pipeline** | Oltalama e-postalarını / URL'lerini sınıflandıran makine öğrenmesi modeli |
| **RAG Sistemi** | Bilgi tabanı üzerinden güçlendirilmiş üretim (Retrieval-Augmented Generation) |
| **Akıllı Ajan** | LangGraph tabanlı otonom analiz ajanı |
| **MCP Sunucusu** | Model Context Protocol ile dış araçlara erişim |
| **Değerlendirme** | Model ve sistem performans metrikleri |

## 📁 Klasör Yapısı

```
oltalama/
├── data/
│   ├── raw/              # Ham veri setleri (git'e dahil edilmez)
│   ├── processed/        # İşlenmiş / temizlenmiş veriler
│   └── kb/               # Bilgi tabanı (knowledge base) dosyaları
├── rag/                  # RAG pipeline bileşenleri
├── ml/                   # ML modeli eğitim & tahmin kodları
├── agent/                # LangGraph ajan tanımları
├── mcp_server/           # MCP sunucu implementasyonu
├── eval/                 # Değerlendirme & metrik scriptleri
├── scripts/              # Yardımcı scriptler
├── config.py             # Merkezi yapılandırma (.env'den okur)
├── 00_kurulum_kontrol.py # Ollama & model bağlantı testi
├── requirements.txt      # Python bağımlılıkları
├── .env.example          # Ortam değişkenleri şablonu
└── README.md             # Bu dosya
```

## 🚀 Kurulum Adımları

### 1. Depoyu klonlayın

```bash
git clone <repo-url>
cd oltalama
```

### 2. Sanal ortam oluşturun

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam değişkenlerini ayarlayın

```bash
cp .env.example .env
# .env dosyasını düzenleyerek kendi ayarlarınızı girin
```

### 5. Ollama'yı kurun ve modelleri indirin

[Ollama](https://ollama.com) kurulumunu tamamladıktan sonra:

```bash
ollama pull nomic-embed-text
ollama pull llama3.1
```

### 6. Kurulum kontrolü

```bash
python 00_kurulum_kontrol.py
```

Tüm testler ✅ ile geçerse sistem kullanıma hazırdır.

## 🛠️ Teknoloji Yığını

- **LLM & Embedding**: Ollama (yerel çalışır, veri dışarı çıkmaz)
- **Vektör Veritabanı**: ChromaDB
- **Orkestrasyon**: LangChain, LangGraph
- **ML**: scikit-learn, pandas
- **Protokol**: Model Context Protocol (MCP)

## 📄 Lisans

Bu proje yalnızca eğitim ve savunma amaçlıdır.
