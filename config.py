"""
Proje yapılandırma dosyası.
Tüm ayarlar .env dosyasından okunur; bulunamazsa varsayılan değerler kullanılır.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# ── Proje kök dizini ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# ── Ollama Ayarları ───────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.1")

# ── Klasör Yolları ────────────────────────────────────────────────
DATA_RAW_DIR = BASE_DIR / os.getenv("DATA_RAW_DIR", "data/raw")
DATA_PROCESSED_DIR = BASE_DIR / os.getenv("DATA_PROCESSED_DIR", "data/processed")
DATA_KB_DIR = BASE_DIR / os.getenv("DATA_KB_DIR", "data/kb")
RAG_DIR = BASE_DIR / os.getenv("RAG_DIR", "rag")
ML_DIR = BASE_DIR / os.getenv("ML_DIR", "ml")
AGENT_DIR = BASE_DIR / os.getenv("AGENT_DIR", "agent")
MCP_SERVER_DIR = BASE_DIR / os.getenv("MCP_SERVER_DIR", "mcp_server")
EVAL_DIR = BASE_DIR / os.getenv("EVAL_DIR", "eval")
SCRIPTS_DIR = BASE_DIR / os.getenv("SCRIPTS_DIR", "scripts")

# ── ChromaDB Ayarları ─────────────────────────────────────────────
CHROMA_PERSIST_DIR = BASE_DIR / os.getenv("CHROMA_PERSIST_DIR", "data/kb/chroma_store")
