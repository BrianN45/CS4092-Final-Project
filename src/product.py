from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int
    active: bool

    @classmethod
    def from_row(cls, row):
        if not row:
            return None

        return cls(
            id=row[0],
            name=row[1],
            price=row[2]/100,
            quantity=row[3],
            active=bool(row[4]),
        )

    def to_db_tuple(self):
        return (self.id, self.name, self.price, self.quantity, int(self.active))
