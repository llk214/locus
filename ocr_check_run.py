import argparse
import fitz
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to a PDF file")
    parser.add_argument("--page", type=int, default=1, help="1-based page number")
    args = parser.parse_args()

    from rapidocr_onnxruntime import RapidOCR

    doc = fitz.open(args.pdf_path)
    page_index = max(args.page - 1, 0)
    page = doc[page_index]
    pix = page.get_pixmap(dpi=200, colorspace=fitz.csRGB)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)

    ocr = RapidOCR()
    result = ocr(img)
    if isinstance(result, tuple):
        result = result[0]
    print(result[:3] if isinstance(result, list) else result)


if __name__ == "__main__":
    main()
