def main():
    try:
        from rapidocr_onnxruntime import RapidOCR
        print("RapidOCR OK:", RapidOCR)
    except Exception as e:
        print("RapidOCR import failed:", e)


if __name__ == "__main__":
    main()
