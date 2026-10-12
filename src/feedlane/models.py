from dataclasses import dataclass, field


@dataclass(frozen=True)
class RawRecord:
    line_number: int
    payload: dict


@dataclass(frozen=True)
class CleanProduct:
    sku: str
    name: str
    category: str
    price_cents: int
    currency: str
    on_hand: int

    def as_dict(self) -> dict:
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "price_cents": self.price_cents,
            "currency": self.currency,
            "on_hand": self.on_hand,
        }


@dataclass(frozen=True)
class RejectedRecord:
    line_number: int
    reason: str
    payload: dict

    def as_dict(self) -> dict:
        return {
            "line_number": self.line_number,
            "reason": self.reason,
            "payload": self.payload,
        }


@dataclass
class RunReport:
    accepted: int = 0
    rejected: int = 0
    reasons: dict[str, int] = field(default_factory=dict)

    def add_reject(self, reason: str) -> None:
        self.rejected += 1
        self.reasons[reason] = self.reasons.get(reason, 0) + 1

    def as_dict(self) -> dict:
        return {
            "accepted": self.accepted,
            "rejected": self.rejected,
            "reasons": self.reasons,
        }
