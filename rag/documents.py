"""
data/kb/ klasöründeki .txt dosyalarını okuyup doküman listesi olarak döndürür.
Her doküman; metin içeriği ve kaynak dosya adı (metadata) içerir.
"""

from pathlib import Path
from dataclasses import dataclass, field
from config import DATA_KB_DIR


@dataclass
class Document:
    """Tek bir bilgi tabanı dokümanını temsil eder."""
    content: str
    metadata: dict = field(default_factory=dict)


def load_documents(kb_dir: Path | None = None) -> list[Document]:
    """
    Bilgi tabanı klasöründeki tüm .txt dosyalarını okur.

    Args:
        kb_dir: Bilgi tabanı klasörü. Belirtilmezse config.DATA_KB_DIR kullanılır.

    Returns:
        Document nesnelerinin listesi.
    """
    kb_dir = kb_dir or DATA_KB_DIR

    if not kb_dir.exists():
        raise FileNotFoundError(f"Bilgi tabanı klasörü bulunamadı: {kb_dir}")

    documents: list[Document] = []

    for file_path in sorted(kb_dir.glob("*.txt")):
        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            continue

        doc = Document(
            content=content,
            metadata={
                "source": file_path.name,
                "path": str(file_path),
            },
        )
        documents.append(doc)

    if not documents:
        print("⚠️  Bilgi tabanı klasöründe .txt dosyası bulunamadı.")

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"📂 Toplam {len(docs)} doküman yüklendi.\n")
    for i, doc in enumerate(docs, 1):
        baslik = doc.content.split("\n")[0] if doc.content else "(boş)"
        print(f"  {i:2d}. [{doc.metadata['source']}]  {baslik}")
