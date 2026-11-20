"""
config.py'deki EMBED_MODEL ayarına göre OllamaEmbeddings istemcisi döndürür.
"""

from langchain_ollama import OllamaEmbeddings
from config import OLLAMA_URL, EMBED_MODEL


def get_embeddings() -> OllamaEmbeddings:
    """
    Ollama embedding istemcisini oluşturur ve döndürür.

    Returns:
        OllamaEmbeddings nesnesi.
    """
    return OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_URL,
    )


if __name__ == "__main__":
    print(f"🧮 Embedding modeli: {EMBED_MODEL}")
    print(f"   Ollama adresi  : {OLLAMA_URL}")

    try:
        emb = get_embeddings()
        test_vector = emb.embed_query("Oltalama nedir?")
        print(f"✅ Embedding çalışıyor! Vektör boyutu: {len(test_vector)}")
    except Exception as e:
        print(f"❌ Embedding hatası: {e}")
