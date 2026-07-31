from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int
    active: bool
    rating: str | None = None

    @classmethod
    def from_row(cls, row):
        if not row:
            return None

        rating = "No Rating"
        if len(row) >= 6 and row[5] is not None:
            rating = row[5]

        return cls(
            id=row[0],
            name=row[1],
            price=row[2] / 100,
            quantity=row[3],
            active=bool(row[4]),
            rating=rating,
        )

    def to_db_tuple(self):
        return (self.id, self.name, self.price, self.quantity, int(self.active))
