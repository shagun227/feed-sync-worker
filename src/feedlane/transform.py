from feedlane.models import CleanProduct, RawRecord, RejectedRecord

REQUIRED = ("sku", "name", "category", "price", "currency")


def normalize(record: RawRecord, category_map: dict[str, str]) -> CleanProduct | RejectedRecord:
    payload = record.payload
    missing = [field for field in REQUIRED if payload.get(field) in (None, "")]
    if missing:
        return RejectedRecord(record.line_number, f"missing {', '.join(missing)}", payload)

    sku = str(payload["sku"]).strip().upper()
    if " " in sku or len(sku) < 2:
        return RejectedRecord(record.line_number, "invalid sku", payload)

    source_category = str(payload["category"]).strip().lower()
    category = category_map.get(source_category)
    if category is None:
        return RejectedRecord(record.line_number, f"unknown category '{source_category}'", payload)

    try:
        price_cents = _money_to_cents(payload["price"])
    except (TypeError, ValueError):
        return RejectedRecord(record.line_number, "invalid price", payload)
    if price_cents < 0:
        return RejectedRecord(record.line_number, "negative price", payload)

    currency = str(payload["currency"]).strip().upper()
    if len(currency) != 3 or not currency.isalpha():
        return RejectedRecord(record.line_number, "invalid currency", payload)

    try:
        on_hand = int(payload.get("on_hand", 0))
    except (TypeError, ValueError):
        return RejectedRecord(record.line_number, "invalid on_hand", payload)
    if on_hand < 0:
        return RejectedRecord(record.line_number, "negative on_hand", payload)

    name = " ".join(str(payload["name"]).split())
    return CleanProduct(
        sku=sku,
        name=name,
        category=category,
        price_cents=price_cents,
        currency=currency,
        on_hand=on_hand,
    )


def _money_to_cents(value) -> int:
    if isinstance(value, bool):
        raise ValueError("price cannot be boolean")
    if isinstance(value, int):
        return value * 100
    if isinstance(value, float):
        return int(round(value * 100))
    text = str(value).strip().replace(",", "")
    if not text:
        raise ValueError("empty price")
    return int(round(float(text) * 100))
