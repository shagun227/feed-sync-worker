from feedlane.models import CleanProduct, RawRecord, RejectedRecord
from feedlane.transform import normalize

CATEGORY_MAP = {"eyewear": "frames", "contacts": "lenses"}


def test_normalize_trims_name_and_converts_price():
    record = RawRecord(
        1,
        {
            "sku": "frame-100",
            "name": "  Harbor   Round ",
            "category": "Eyewear",
            "price": "89.00",
            "currency": "inr",
            "on_hand": "3",
        },
    )
    result = normalize(record, CATEGORY_MAP)
    assert isinstance(result, CleanProduct)
    assert result.sku == "FRAME-100"
    assert result.name == "Harbor Round"
    assert result.category == "frames"
    assert result.price_cents == 8900
    assert result.currency == "INR"
    assert result.on_hand == 3


def test_unknown_category_is_rejected():
    record = RawRecord(
        2,
        {"sku": "CASE-1", "name": "Case", "category": "accessories", "price": 10, "currency": "INR"},
    )
    result = normalize(record, CATEGORY_MAP)
    assert isinstance(result, RejectedRecord)
    assert "unknown category" in result.reason
