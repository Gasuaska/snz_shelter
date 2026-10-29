from io import BytesIO

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject


def arrange_four_per_a4(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    writer = PdfWriter()

    a4_width = 595.28
    a4_height = 841.89

    half_width = a4_width / 2
    half_height = a4_height / 2

    positions = [
        (0, half_height),
        (half_width, half_height),
        (0, 0),
        (half_width, 0),
    ]

    for start in range(0, len(reader.pages), 4):
        sheet = PageObject.create_blank_page(
            width=a4_width,
            height=a4_height,
        )

        for index, page in enumerate(reader.pages[start:start + 4]):
            x, y = positions[index]

            scale = min(
                half_width / float(page.mediabox.width),
                half_height / float(page.mediabox.height),
            )

            transform = (
                Transformation()
                .scale(scale)
                .translate(x, y)
            )

            sheet.merge_transformed_page(page, transform)

        writer.add_page(sheet)

    output = BytesIO()
    writer.write(output)

    return output.getvalue()