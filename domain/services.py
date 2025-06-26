from typing import List, Optional
from .models import Product, Order
from .repositories import ProductRepository, OrderRepository
from .unit_of_work import UnitOfWork


class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository,
                 uow: UnitOfWork):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.uow = uow

    def create_product(self, name: str, quantity: int, price: float, is_active: bool = True) \
            -> Product:
        product = Product(id=None, name=name, quantity=quantity, price=price, is_active=is_active)
        self.product_repo.add(product)
        self.uow.commit()
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.product_repo.get(product_id)

    def _list_products(self) -> List[Product]:
        return self.product_repo.list()

    def update_product(self, product_id: int, name: str = None,
                       quantity: int = None, price: float = None) -> Product:
        product = self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        if name is not None:
            product.name = name
        if quantity is not None:
            product.quantity = quantity
        if price is not None:
            product.price = price

        self.product_repo.update(product)
        self.uow.commit()
        return product

    def delete_product(self, product_id: int) -> None:
        self.product_repo.delete(product_id)

    def create_order(self, product_ids: List[int], address: str) -> Order:
        products = []
        for product_id in product_ids:
            product = self.product_repo.get(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            products.append(product)

        order = Order(
            id=None,
            products=products,
            address=address
        )
        self.order_repo.add(order)
        self.uow.commit()
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.order_repo.get(order_id)

    def list_orders(self) -> List[Order]:
        return self.order_repo.list()

    def update_order(self, order_id: int, product_ids: List[int]) -> Order:
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")

        products = []
        for product_id in product_ids:
            product = self.product_repo.get(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            products.append(product)

        order.products = products
        self.order_repo.update(order)
        return order

    def delete_order(self, order_id: int) -> None:
        self.order_repo.delete(order_id)

    def add_product_to_order(self, order_id: int, product_id: int) -> Order:
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")

        product = self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        if product not in order.products:
            order.products.append(product)
            self.order_repo.update(order)

        return order

    def remove_product_from_order(self, order_id: int, product_id: int) -> Order:
        order = self.order_repo.get(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")

        product = self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        order.products = [p for p in order.products if p.id != product_id]
        self.order_repo.update(order)
        return order
