import requests

BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    print(response.json())


def view_one_item():
    item_id = input("Enter item ID: ")

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    print(response.json())

def add_item():
    item = {
        "barcode": input("Enter barcode: "),
        "product_name": input("Enter product name: "),
        "brands": input("Enter brand: "),
        "ingredients_text": input("Enter ingredients: "),
        "quantity": int(input("Enter quantity: ")),
        "price": int(input("Enter price: "))
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=item
    )

    print(response.json())

def update_item():
    item_id = input("Enter item ID to update: ")

    quantity = input("Enter new quantity: ")
    price = input("Enter new price: ")

    data = {}

    if quantity:
        data["quantity"] = int(quantity)

    if price:
        data["price"] = int(price)

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    print(response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ")

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")

    print(response.json())


def main():
    while True:
        print("\nInventory Management System")
        print("1. View inventory")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_one_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()