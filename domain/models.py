import datetime
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float
    is_active: bool = field(default=True)

@dataclass
class Order:
    id: int
    address : str
    create_datetime : datetime = field(default_factory=datetime.datetime.now)
    update_datetime : datetime = field(default_factory=datetime.datetime.now)
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)
