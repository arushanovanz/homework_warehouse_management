from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Product, Order


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> None:
        pass

    @abstractmethod
    def get(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        pass

    @abstractmethod
    def get(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        pass

    @abstractmethod
    def delete_one_quantity_product(self, order: Order, product: Product) -> Order:
        pass

    @abstractmethod
    def delete_product(self, order: Order, product: Product) -> Order:
        pass
