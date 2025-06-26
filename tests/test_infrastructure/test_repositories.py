import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from domain.models import Product, Order
from datetime import datetime


@pytest.fixture
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_product_repository(test_session):
    repo = SqlAlchemyProductRepository(test_session)

    product = Product(
        id=None,
        name="Test",
        quantity=5,
        price=10.5,
        is_active=True
    )
    repo.add(product)
    test_session.commit()

    assert product.id is not None


    retrieved = repo.get(product.id)
    assert retrieved.name == "Test"
    assert retrieved.quantity == 5


    products = repo.list()
    assert len(products) == 1
    assert products[0].id == product.id


def test_order_repository(test_session):

    product_repo = SqlAlchemyProductRepository(test_session)
    p1 = Product(id=None, name="P1", quantity=1, price=10, is_active=True)
    p2 = Product(id=None, name="P2", quantity=2, price=20, is_active=True)
    product_repo.add(p1)
    product_repo.add(p2)
    test_session.commit()


    order_repo = SqlAlchemyOrderRepository(test_session)
    order = Order(
        id=None,
        products=[p1, p2],
        address="Test Address",
        create_datetime=datetime.now(),
        update_datetime=datetime.now()
    )
    order_repo.add(order)
    test_session.commit()

    assert order.id is not None


    retrieved = order_repo.get(order.id)
    assert retrieved.address == "Test Address"
    assert len(retrieved.products) == 2
    assert retrieved.products[0].name == "P1"