"""
Dokümanları RecursiveCharacterTextSplitter ile paragraf ve cümle
sınırlarına uygun şekilde 400 karakterlik, 60 karakter örtüşmeli
parçalara böler. Her chunk kaynak dosya adını metadata olarak taşır.
"""

from dataclasses import dataclass, field
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag.documents import Document

# ── Parçalama Ayarları ─────────────────────────────────────────────
CHUNK_SIZE = 400
CHUNK_OVERLAP = 60
SEPARATORS = ["\n\n", "\n", ". ", " "]


@dataclass
class Chunk:
    """Bir doküman parçasını temsil eder."""
    content: str
    metadata: dict = field(default_factory=dict)


def split_into_chunks(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """
    Doküman listesini paragraf ve cümle sınırlarına uygun parçalara böler.

    RecursiveCharacterTextSplitter önce '\\n\\n' (paragraf), sonra '\\n' (satır),
    ardından '. ' (cümle), son olarak ' ' (kelime) sınırlarından böler.
    Böylece kelime ortasında kesme yapılmaz.

    Args:
        documents: Document nesnelerinin listesi.
        chunk_size: Her parçanın maksimum karakter sayısı.
        chunk_overlap: Ardışık parçalar arasındaki örtüşme karakter sayısı.

    Returns:
        Chunk nesnelerinin listesi.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=SEPARATORS,
        length_function=len,
        is_separator_regex=False,
    )

    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.content.strip()
        if not text:
            continue

        parts = splitter.split_text(text)

        for idx, part in enumerate(parts):
            chunk = Chunk(
                content=part,
                metadata={
                    **doc.metadata,
                    "chunk_index": idx,
                },
            )
            chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    from rag.documents import load_documents

    docs = load_documents()
    all_chunks = split_into_chunks(docs)

    print(f"📄 {len(docs)} doküman → 🧩 {len(all_chunks)} chunk")
    print(f"   Chunk boyutu  : {CHUNK_SIZE} karakter")
    print(f"   Örtüşme       : {CHUNK_OVERLAP} karakter")
    print(f"   Ayırıcılar    : {SEPARATORS}\n")

    # İlk 3 chunk'ı örnek göster
    for i, chunk in enumerate(all_chunks[:3], 1):
        print(f"  ── Chunk {i} [{chunk.metadata['source']}] ({len(chunk.content)} kar.) ──")
        print(f"  {chunk.content[:200]}")
        print()
