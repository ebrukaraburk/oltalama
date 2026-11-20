"""
Chunk'ları embedding'e çevirip ChromaDB'ye kalıcı olarak kaydeder.
Tekrar çalıştırıldığında mevcut koleksiyonu temizleyip yeniden indeksler,
böylece kopya oluşmaz.

Kullanım:
    python -m rag.index
"""

import chromadb
from config import BASE_DIR
from rag.documents import load_documents
from rag.chunks import split_into_chunks
from rag.embeddings import get_embeddings

# ── ChromaDB Ayarları ──────────────────────────────────────────────
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "oltalama_kb"


def build_index(force_rebuild: bool = True) -> None:
    """
    Bilgi tabanını ChromaDB'ye indeksler.

    Args:
        force_rebuild: True ise mevcut koleksiyonu silip yeniden oluşturur.
    """
    # 1) Dokümanları yükle ve parçala
    print("📂 Dokümanlar yükleniyor...")
    docs = load_documents()
    chunks = split_into_chunks(docs)
    print(f"   {len(docs)} doküman → {len(chunks)} chunk\n")

    if not chunks:
        print("⚠️  İndekslenecek chunk bulunamadı.")
        return

    # 2) ChromaDB istemcisi
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 3) Kopya önleme: mevcut koleksiyonu sil ve yeniden oluştur
    if force_rebuild:
        existing = [c.name for c in client.list_collections()]
        if COLLECTION_NAME in existing:
            client.delete_collection(COLLECTION_NAME)
            print(f"🗑️  Mevcut '{COLLECTION_NAME}' koleksiyonu silindi (kopya önleme).")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # 4) Embedding istemcisi
    print("🧮 Embedding modeli hazırlanıyor...")
    embeddings_client = get_embeddings()

    # 5) Chunk'ları toplu olarak embed et ve kaydet
    print("⏳ Chunk'lar indeksleniyor...")

    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]

        texts = [c.content for c in batch]
        metadatas = [c.metadata for c in batch]
        ids = [f"chunk_{i + j}" for j in range(len(batch))]

        # Embedding'leri hesapla
        vectors = embeddings_client.embed_documents(texts)

        # ChromaDB'ye ekle
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=vectors,
            metadatas=metadatas,
        )

        print(f"   ✓ {min(i + batch_size, len(chunks))}/{len(chunks)} chunk indekslendi")

    print(f"\n✅ İndeksleme tamamlandı!")
    print(f"   Koleksiyon : {COLLECTION_NAME}")
    print(f"   Kayıt sayısı: {collection.count()}")
    print(f"   Depolama    : {CHROMA_DIR}")


if __name__ == "__main__":
    build_index()
