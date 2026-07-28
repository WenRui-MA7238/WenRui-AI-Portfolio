import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Union


class PDFLoader:
    """PDF 转图片"""

    def __init__(self, dpi: int = 200):
        self.dpi = dpi

    def to_images(self, pdf_path: Union[str, Path], output_dir: Union[str, Path]) -> List[Path]:
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf_path)
        paths = []
        for i, page in enumerate(doc):
            mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            out_path = output_dir / f"{pdf_path.stem}_page_{i + 1}.png"
            pix.save(out_path)
            paths.append(out_path)
        doc.close()
        return paths
