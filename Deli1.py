# Dictionary to store products by their unique product ID Hash Table equivalent for lookup 
# by product ID
inventory = {}

# Dictionary to store categories and their corresponding product IDs
#  mapping each category to a list of product IDs (uses lists for each category
categories = {}

def add_product(product_id, name, quantity, price, category):
    """
    Adds a new product to the inventory and updates the category mapping.
    """
    # Product information stored in a dictionary
    product = {
        'name': name,
        'quantity': quantity,
        'price': price,
        'category': category
    }
    # Add product to the inventory
    inventory[product_id] = product

    # Update category mapping
    if category not in categories:
        categories[category] = []
    categories[category].append(product_id)


def update_product(product_id, quantity=None, price=None):
    """
    Updates the quantity and/or price of an existing product.
    """
    if product_id in inventory:
        if quantity is not None:
            inventory[product_id]['quantity'] = quantity
        if price is not None:
            inventory[product_id]['price'] = price
    else:
        print("Product not found in inventory.")


def remove_product(product_id):
    """
    Removes a product from the inventory and updates the category mapping.
    """
    if product_id in inventory:
        category = inventory[product_id]['category']
        # Remove product from the category list
        categories[category].remove(product_id)
        # If category list is empty, remove the category
        if not categories[category]:
            del categories[category]
        # Remove product from inventory
        del inventory[product_id]
    else:
        print("Product not found in inventory.")


def get_product(product_id):
    """
    Retrieves a product's details from the inventory by its product ID.
    """
    return inventory.get(product_id, "Product not found.")


def get_products_by_category(category):
    """
    Retrieves a list of products for a specific category.
    """
    product_ids = categories.get(category, [])
    return [inventory[pid] for pid in product_ids]


def display_inventory():
    """
    Displays the entire inventory.
    """
    print(f"Inventory: {len(inventory)} products.")
    for product_id, product_info in inventory.items():
        print(f"ID: {product_id}, {product_info}")




def search_products(name=None, price_range=None, category=None):
    results = []
    for product_id, product in inventory.items():
        if name and name.lower() not in product['name'].lower():
            continue
        if price_range:
            min_price, max_price = price_range
            if not (min_price <= product['price'] <= max_price):
                continue
        if category and product['category'] != category:
            continue
        results.append({'product_id': product_id, **product})
    return results


# Example usage
add_product(1, "Laptop", 10, 999.99, "Electronics")
add_product(2, "Phone", 25, 499.99, "Electronics")
add_product(3, "Chair", 50, 79.99, "Furniture")


print("\nProducts in 'Electronics' Category:", get_products_by_category("Electronics"))

print("\nSearch by Name (Laptop):")
print(search_products(name="a"))