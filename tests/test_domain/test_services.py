import pytest
from unittest.mock import Mock
from domain.services import WarehouseService
from domain.models import Product, Order
from domain.repositories import ProductRepository, OrderRepository
from domain.unit_of_work import UnitOfWork


@pytest.fixture
def mock_repos():
    product_repo = Mock(spec=ProductRepository)
    order_repo = Mock(spec=OrderRepository)
    uow = Mock(spec=UnitOfWork)
    return product_repo, order_repo, uow


def test_create_product(mock_repos):
    product_repo, order_repo, uow = mock_repos

    test_product = Product(id=1, name="Test", quantity=5, price=10.5, is_active=True)
    product_repo.add.return_value = None

    service = WarehouseService(product_repo, order_repo, uow)

    result = service.create_product("Test", 5, 10.5)

    assert result.name == "Test"
    product_repo.add.assert_called_once()
    uow.commit.assert_called_once()


def test_create_order(mock_repos):
    product_repo, order_repo, uow = mock_repos


    p1 = Product(id=1, name="P1", quantity=1, price=10, is_active=True)
    p2 = Product(id=2, name="P2", quantity=2, price=20, is_active=True)
    product_repo.get.side_effect = [p1, p2]


    service = WarehouseService(product_repo, order_repo, uow)

    result = service.create_order([1, 2], "Test Address")

    assert len(result.products) == 2
    assert result.address == "Test Address"
    order_repo.add.assert_called_once()
    uow.commit.assert_called_once()