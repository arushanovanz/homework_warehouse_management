from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class WarehouseConsoleUI:
    def __init__(self, warehouse_service: WarehouseService):
        self.service = warehouse_service

    def show_menu(self):
        while True:
            print("\n=== Warehouse Management System ===")
            print("1. Add Product")
            print("2. List Products")
            print("3. Create Order")
            print("4. List Orders")
            print("5. Edit Order (add/remove products)")
            print("6. Delete Order")
            print("7. Delete Product")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self._add_product()
            elif choice == "2":
                self._list_products()
            elif choice == "3":
                self._create_order()
            elif choice == "4":
                self._list_orders()
            elif choice == "5":
                self._edit_order()
            elif choice == "6":
                self._delete_order()
            elif choice == "7":
                self._delete_product()
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again")

    def _add_product(self):
        print("\n--- Add New Product ---")
        name = input("Product name: ")
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        is_active = input("Is active? (y/n): ").lower() == 'y'

        product = self.service.create_product(name, quantity, price, is_active)
        print(f"Product created: ID {product.name}")

    def _list_products(self):
        print("\n--- Product List ---")
        products = self.service._list_products()
        for p in products:
         print(f"ID: {p.id}, Name: {p.name}, Quantity: {p.quantity}, Price: {p.price}")


    def _create_order(self):
        print("\n--- Create New Order ---")
        self._list_products()
        product_ids = []
        while True:
            product_id = input("Enter product ID to add (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            try:
                product_ids.append(int(product_id))
            except ValueError:
                print("Please enter a valid number or 'done'")

        if not product_ids:
            print("Order must contain at least one product")
            return

        address = input("Delivery address: ").strip()

        order = self.service.create_order(product_ids, address)
        print(f"Order created: ID {order.id}")


    def _list_orders(self):
        print("\n--- Order List ---")
        orders = self.service.list_orders()
        for o in orders:
            print(f"\nOrder ID: {o.id}")
            print("Products:")
            for p in o.products:
                print(f"  - {p.name} (ID: {p.id}, Qty: {p.quantity}, Price: {p.price})")


    def _edit_order(self):
        print("\n--- Edit Order ---")
        self._list_orders()
        try:
            order_id = int(input("Enter order ID to edit: "))
            order = self.service.get_order(order_id)
            if not order:
                print("Order not found")
                return

            print("\nCurrent order products:")
            for p in order.products:
                print(f"ID: {p.id}, Name: {p.name}")

            print("\n1. Add product to order")
            print("2. Remove product from order")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                self._list_products()
                product_id = int(input("Enter product ID to add: "))
                updated_order = self.service.add_product_to_order(order_id, product_id)
                print("Product added to order")
            elif sub_choice == "2":
                product_id = int(input("Enter product ID to remove: "))
                updated_order = self.service.remove_product_from_order(order_id, product_id)
                print("Product removed from order")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")


    def _delete_order(self):
        print("\n--- Delete Order ---")
        self._list_orders()
        try:
            order_id = int(input("Enter order ID to delete: "))
            self.service.delete_order(order_id)
            print("Order deleted")
        except ValueError:
            print("Please enter a valid number")


    def _delete_product(self):
        print("\n--- Delete Product ---")
        self._list_products()
        try:
            product_id = int(input("Enter product ID to delete: "))
            self.service.delete_product(product_id)
            print("Product deleted")
        except ValueError:
            print("Please enter a valid number")


def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)
    with uow:
        service = WarehouseService(product_repo, order_repo)
        ui = WarehouseConsoleUI(service)
        ui.show_menu()


if __name__ == "__main__":
    main()
