import logging
from typing import List

from sqlalchemy.orm import Session

from domain.models import Order, Product
from domain.repositories import ProductRepository, OrderRepository
from .orm import ProductORM, OrderORM


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product):
        product_orm = ProductORM(
            name=product.name,
            quantity=product.quantity,
            price=product.price,
            is_active=True
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id

    def get(self, product_id: int) -> Product:
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
            is_active=product_orm.is_active
        )

    def list(self) -> List[Product]:
        products_orm = self.session.query(ProductORM).filter_by(is_active=True).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]

    def update(self, product: Product) -> None:
        product_orm = self.session.query(ProductORM).get(product.id)
        if product_orm:
            product_orm.name = product.name
            product_orm.quantity = product.quantity
            product_orm.price = product.price
            product_orm.is_active = product.is_active
            self.session.add(product_orm)

    def delete(self, product_id: int) -> None:
        product_orm = self.session.query(ProductORM).get(product_id)
        if product_orm:
            self.session.delete(product_orm)


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order) -> None:
        order_orm = OrderORM(
            address=order.address
        )
        order_orm.products = [
            self.session.query(ProductORM).get(p.id)
            for p in order.products
        ]

        order.create_datetime = order_orm.create_datetime
        order.update_datetime = order_orm.update_datetime
        self.session.add(order_orm)
        self.session.flush()
        order.id = order_orm.id


    def get(self, order_id: int) -> Order:
        order_orm = self.session.query(OrderORM).get(order_id)
        if order_orm is None:
            return None
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price, is_active=p.is_active)
            for p in order_orm.products
        ]
        return Order(
            id=order_orm.id,
            products=products,
            create_datetime=order_orm.create_datetime,
            update_datetime=order_orm.update_datetime,
            address=order_orm.address
        )

    def list(self) -> List[Order]:
        orders_orm = self.session.query(OrderORM).filter_by(is_deleted=False).all()
        orders = []
        for order_orm in orders_orm:
            products = [
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
                for p in order_orm.products
            ]
            orders.append(Order(id=order_orm.id, products=products, create_datetime=order_orm.create_datetime,
                                update_datetime=order_orm.update_datetime,
                                address=order_orm.address))
        return orders

    def delete_product(self, order: Order, product: Product) -> Order:
        if product not in order.products:
            raise ValueError(f"Product {product.id} with {product.name} not found in order # {order.id}")
        for p in order.products:
            if p.id == product.id:
                self.session.delete(product)
        return Order(id=order.id, products=order.products, create_datetime=order.create_datetime,
                     update_datetime=order.update_datetime,
                     address=order.address)

    def delete_one_quantity_product(self, order: Order, product: Product) -> Order:
        if product not in order.products:
            raise ValueError(f"Product {product.id} with {product.name} not found in order # {order.id}")
        for p in order.products:
            if p.id == p.id:
                if p.quantity < 1:
                    logging.info(f"Nothing to delete from order")
                else:
                    p.quantity -= p.quantity
        return Order(id=order.id, products=order.products, create_datetime=order.create_datetime,
                     update_datetime=order.update_datetime,
                     address=order.address)

    def update(self, order: Order) -> None:
        order_orm = self.session.query(OrderORM).get(order.id)
        if order_orm:
            order_orm.products = [
                self.session.query(ProductORM).get(p.id)
                for p in order.products
            ]
            self.session.add(order_orm)

    def delete(self, order_id: int) -> None:
        order_orm = self.session.query(OrderORM).get(order_id)
        if order_orm:
            order_orm.is_deleted = True
            self.session.commit()
