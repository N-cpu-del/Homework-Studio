import fitz


class PdfExtractionError(Exception):
    pass


def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf",
        )

    except Exception as exc:
        raise PdfExtractionError(
            "PDF could not be opened."
        ) from exc


    try:
        pages: list[str] = []

        for index, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append(
                    f"[Page {index}]\n{text}"
                )

    finally:
        document.close()


    combined = "\n\n".join(pages).strip()


    if not combined:
        raise PdfExtractionError(
            "PDF contains no extractable text."
        )


    return combined