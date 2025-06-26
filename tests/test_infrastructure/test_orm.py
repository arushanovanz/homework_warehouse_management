import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm import Base, ProductORM, OrderORM
from datetime import datetime


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_product_orm_creation(db_session):

    product = ProductORM(name="Test Product", quantity=10, price=99.99)
    db_session.add(product)
    db_session.commit()

    assert product.id is not None
    assert product.name == "Test Product"
    assert product.quantity == 10
    assert product.price == 99.99
    assert product.is_active is True
    assert isinstance(product.update_datetime, datetime)


def test_order_orm_creation(db_session):

    p1 = ProductORM(name="P1", quantity=5, price=10)
    p2 = ProductORM(name="P2", quantity=3, price=20)
    db_session.add_all([p1, p2])
    db_session.commit()


    order = OrderORM(address="Test Address")
    order.products = [p1, p2]
    db_session.add(order)
    db_session.commit()

    assert order.id is not None
    assert order.address == "Test Address"
    assert len(order.products) == 2
    assert order.products[0].name == "P1"
    assert isinstance(order.create_datetime, datetime)