"""
Bir sorgu metni alıp ChromaDB'den en benzer 3 chunk'ı,
kaynak adı ve benzerlik skoruyla birlikte getirir.

Kullanım:
    python -m rag.search
"""

import chromadb
from config import BASE_DIR
from rag.embeddings import get_embeddings

# ── Ayarlar ────────────────────────────────────────────────────────
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "oltalama_kb"
TOP_K = 3


def search(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Sorgu metnine en benzer chunk'ları ChromaDB'den getirir.

    Args:
        query: Arama sorgusu metni.
        top_k: Döndürülecek sonuç sayısı.

    Returns:
        Her biri 'content', 'source', 'score' ve 'metadata' içeren sözlük listesi.
    """
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"ChromaDB veritabanı bulunamadı: {CHROMA_DIR}\n"
            "Önce 'python -m rag.index' komutunu çalıştırarak indeksleme yapın."
        )

    # ChromaDB bağlantısı
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    # Sorgu embedding'i oluştur
    embeddings_client = get_embeddings()
    query_vector = embeddings_client.embed_query(query)

    # Benzerlik araması
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Sonuçları düzenle
    output = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        # ChromaDB cosine distance → benzerlik skoru (1 - distance)
        similarity = 1 - distance

        output.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "bilinmiyor"),
            "score": round(similarity, 4),
            "metadata": results["metadatas"][0][i],
        })

    return output


def interactive_search() -> None:
    """Komut satırından etkileşimli arama yapar."""
    print("\n" + "=" * 60)
    print("  🔍 Oltalama Bilgi Tabanı Arama")
    print("  Çıkmak için 'q' veya 'çık' yazın.")
    print("=" * 60)

    while True:
        print()
        query = input("Sorgunuz: ").strip()

        if not query:
            continue
        if query.lower() in ("q", "çık", "exit", "quit"):
            print("👋 Görüşmek üzere!")
            break

        try:
            results = search(query)
        except Exception as e:
            print(f"❌ Arama hatası: {e}")
            continue

        if not results:
            print("  Sonuç bulunamadı.")
            continue

        print(f"\n  📋 En benzer {len(results)} sonuç:\n")
        for i, r in enumerate(results, 1):
            print(f"  ── {i}. Sonuç (Benzerlik: {r['score']:.4f}) ──")
            print(f"  📄 Kaynak: {r['source']}")
            print(f"  {r['content'][:300]}")
            if len(r['content']) > 300:
                print(f"  ... ({len(r['content'])} karakter)")
            print()


if __name__ == "__main__":
    interactive_search()
