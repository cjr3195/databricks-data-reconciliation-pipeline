import re


def clean_reference_address(
    value,
):

    if value is None:
        return ""

    text = str(value).strip()

    if not text:
        return ""

    parts = [
        part.strip()
        for part in text.split(",")
        if part.strip()
    ]

    if not parts:
        return ""

    start_index = None

    for index, part in enumerate(parts):
        if re.match(r"^\d", part):
            start_index = index
            break

    if start_index is not None:
        parts = parts[start_index:]

    return re.sub(
        r"\s+",
        " ",
        ", ".join(parts),
    ).strip()
