import argparse
import fitz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to a PDF file")
    parser.add_argument("--page", type=int, default=1, help="1-based page number")
    args = parser.parse_args()

    doc = fitz.open(args.pdf_path)
    page_index = max(args.page - 1, 0)
    page = doc[page_index]
    count = len(page.get_images(full=True))
    print(f"Images on page {args.page}: {count}")


if __name__ == "__main__":
    main()
