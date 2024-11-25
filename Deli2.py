import gc
import tracemalloc
import time

# Data structures
inventory = {}
categories = {}

# Enable memory profiling
def start_memory_profiler():
    tracemalloc.start()
    print("Memory profiling started.")

def stop_memory_profiler():
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")

def memory_profiling():
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")

def trigger_gc():
    gc.collect()
    print("Garbage collection triggered.")

# Core operations
def add_product(product_id, name, quantity, price, category):
    product = {'name': name, 'quantity': quantity, 'price': price, 'category': category}
    inventory[product_id] = product
    if category not in categories:
        categories[category] = []
    categories[category].append(product_id)

def update_product(product_id, quantity=None, price=None):
    if product_id in inventory:
        if quantity is not None:
            inventory[product_id]['quantity'] = quantity
        if price is not None:
            inventory[product_id]['price'] = price
    else:
        print("Product not found in inventory.")

def remove_product(product_id):
    if product_id in inventory:
        category = inventory[product_id]['category']
        categories[category].remove(product_id)
        if not categories[category]:
            del categories[category]
        del inventory[product_id]
    else:
        print("Product not found in inventory.")


#Retrieve products
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



# Search functionalities
def search_by_name(name):
    return [product for product in inventory.values() if name.lower() in product['name'].lower()]

def search_by_price_range(min_price, max_price):
    return [product for product in inventory.values() if min_price <= product['price'] <= max_price]

def search_by_category(category):
    """
    Search for all products in a specific category.
    :param category: The category to search for.
    :return: A list of products in the specified category.
    """
    return [product for product in inventory.values() if product['category'] == category]


# Sorting functionalities
def sort_products_by_key(key, reverse=False):
    return sorted(inventory.items(), key=lambda x: x[1][key], reverse=reverse)

# Display inventory
def display_inventory():
    print(f"Inventory: {len(inventory)} products.")
    for product_id, product_info in inventory.items():
        print(f"ID: {product_id}, {product_info}")



# Tests and validation
def run_tests():
    print("Running tests...")
    add_product(101, "Test Laptop", 5, 1500, "Electronics")
    assert get_product(101)['name'] == "Test Laptop", "Add Product Test Failed"
    update_product(101, quantity=10)
    assert get_product(101)['quantity'] == 10, "Update Product Test Failed"
    remove_product(101)
    assert get_product(101) == "Product not found.", "Remove Product Test Failed"
    search_functionality_tests()
    large_inventory_test()
    print("All tests passed successfully!")

def search_functionality_tests():
    add_product(201, "Smartphone", 20, 500, "Electronics")
    add_product(202, "Tablet", 15, 300, "Electronics")
    add_product(203, "Smartwatch", 25, 150, "Wearables")
    add_product(204, "Laptop", 10, 1000, "Electronics")
    results = search_by_name("Smart")
    assert len(results) == 2, "Search by name test failed"
    results = search_by_price_range(100, 400)
    assert len(results) == 2, "Search by price range test failed"
    for pid in [201, 202, 203, 204]:
        remove_product(pid)

def large_inventory_test():
    start_time = time.time()
    for i in range(1, 100001):
        add_product(i, f"Product {i}", i * 2, i * 10.5, "Category A" if i % 2 == 0 else "Category B")
    end_time = time.time()
    print(f"Time to add 100,000 products: {end_time - start_time:.2f} seconds")
    trigger_gc()
    memory_profiling()
    for i in range(1, 100001):
        remove_product(i)


# Stress and scalability testing
def stress_test():
    print("Starting stress test...")
    tracemalloc.start()

    for num_products in [10000, 50000, 100000]:
        print(f"\nTesting with {num_products} products...")
        # Add products
        for i in range(num_products):
            add_product(i, f"Product{i}", i * 2, i * 10.5, "CategoryA" if i % 2 == 0 else "CategoryB")
        
        # Measure search by name
        target_name = f"Product{num_products - 1}"
        start_time = time.time()
        result = search_by_name(target_name)
        search_name_time = time.time() - start_time
        print(f"Time to search by name '{target_name}': {search_name_time:.6f} seconds.")

        # Measure search by category
        target_category = "CategoryA"
        start_time = time.time()
        results = search_by_category(target_category)
        search_category_time = time.time() - start_time
        print(f"Time to search by category '{target_category}': {search_category_time:.6f} seconds.")

        # Measure search by price range
        price_min, price_max = 500, 1500
        start_time = time.time()
        results = search_by_price_range(price_min, price_max)
        search_price_time = time.time() - start_time
        print(f"Time to search by price range ({price_min}, {price_max}): {search_price_time:.6f} seconds.")

        # Measure memory
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory usage: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")

        # Cleanup
        for i in range(num_products):
            remove_product(i)
        gc.collect()


def scalability_test():
    sizes = [10000, 50000, 100000]
    for size in sizes:
        print(f"Testing with {size} products...")
        tracemalloc.start()
        start_time = time.time()
        for i in range(1, size + 1):
            add_product(i, f"Product {i}", i * 2, i * 10.5, "Category B")
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Time: {end_time - start_time:.2f}s; Memory: {peak / 1024 / 1024:.2f} MB")
        for i in range(1, size + 1):
            remove_product(i)

    tracemalloc.stop()
    print("Stress test completed.")



#Run tests
if __name__ == "__main__":
    start_memory_profiler()
    run_tests()
    stress_test()
    scalability_test()
    stop_memory_profiler()
